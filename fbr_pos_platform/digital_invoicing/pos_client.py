"""
========================================================
digital_invoicing/pos_client.py

FBR Retail POS (IMS) API Client

Handles communication with FBR Retail POS Cloud API.
Separate from Digital Invoicing (DI) API - different endpoints,
authentication, and payload structure.

FBR POS Endpoints:
- Sandbox: https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData
- Production: https://gw.fbr.gov.pk/imsp/v1/api/Live/PostData

Authentication: Bearer token + POSID
========================================================
"""

import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def resolve_pos_endpoint(company: object, is_sandbox: bool = True) -> str:
    """Return the POS endpoint configured for the requested environment."""
    if is_sandbox:
        endpoint = getattr(company, "pos_sandbox_endpoint", "") or ""
    else:
        endpoint = getattr(company, "pos_production_endpoint", "") or ""

    if endpoint:
        return endpoint

    fallback = getattr(company, "pos_sandbox_endpoint", "") or ""
    if fallback:
        return fallback

    return "https://gw.fbr.gov.pk/imsp/v1/api/Live/PostData" if not is_sandbox else "https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData"


class POSAPIError(Exception):
    """
    FBR POS API error.
    
    FBR POS API returns errors in the response body.
    """
    def __init__(self, error_code: str, message: str, raw_response: dict = None):
        self.error_code = error_code
        self.message = message
        self.raw_response = raw_response or {}
        super().__init__(f"[{error_code}] {message}")


class POSClient:
    """
    FBR Retail POS API client.
    
    Handles invoice submission to FBR POS Cloud API.
    Uses POSID + Access Code for authentication.
    """
    
    def __init__(
        self,
        pos_id: str,
        access_code: str,
        base_url: str,
        is_sandbox: bool = True
    ):
        """
        Initialize POS client.
        
        Args:
            pos_id: POS Registration Number (from FBR)
            access_code: Access Code for POS integration
            base_url: FBR POS API endpoint
            is_sandbox: True for sandbox, False for production
        """
        self.pos_id = pos_id
        self.access_code = access_code
        self.base_url = base_url
        self.is_sandbox = is_sandbox
        self.timeout = 90  # seconds
    
    def _headers(self) -> dict:
        """
        Build request headers.
        
        FBR POS API uses Bearer token authentication.
        """
        return {
            "Authorization": f"Bearer {self.access_code}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def _check_response_errors(self, response_data: dict) -> None:
        """
        Parse FBR POS API response for errors.
        
        FBR POS API response structure:
        {
            "InvoiceNumber": "1234567890",  (or "Not Available" on error)
            "Code": "100",                  (or "102" on error)
            "Response": "Successfully saved" (or error message)
        }
        """
        if not isinstance(response_data, dict):
            return
            
        # WSO2 Gateway Errors (like 900908)
        fault = response_data.get("fault", {})
        if fault:
            raise POSAPIError(
                error_code=str(fault.get("code", "UNK")),
                message=fault.get("message", "") + " - " + fault.get("description", ""),
                raw_response=response_data
            )
        
        # FBR POS API Application Errors
        code = str(response_data.get("Code", ""))
        fbr_invoice_number = str(response_data.get("InvoiceNumber", ""))
        
        if fbr_invoice_number.lower() == "not available" or not fbr_invoice_number:
            error_message = response_data.get("Response", "FBR did not return a valid invoice number")
            raise POSAPIError(
                error_code=code or "UNK",
                message=error_message,
                raw_response=response_data
            )
            
    def submit_invoice(self, payload: dict) -> dict:
        """
        Submit invoice to FBR POS API.
        
        Args:
            payload: FBR POS invoice JSON payload
            
        Returns:
            dict with:
                - fbr_invoice_number: FBR-generated invoice number
                - raw_response: Full FBR response
                
        Raises:
            POSAPIError: If FBR returns an error
            requests.RequestException: If network error occurs
        """
        logger.info(
            f"[POS Client] Submitting invoice to {'SANDBOX' if self.is_sandbox else 'PRODUCTION'} "
            f"POS ID: {self.pos_id}"
        )
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self._headers(),
                timeout=self.timeout,
                verify=True,
            )
            response.raise_for_status()
            
            response_data = response.json()
            
            # Check for FBR errors (will raise POSAPIError if it failed)
            self._check_response_errors(response_data)
            
            # Extract invoice number
            fbr_invoice_number = str(response_data.get("InvoiceNumber", ""))
            
            logger.info(
                f"[POS Client] ✓ Invoice submitted successfully. "
                f"FBR Invoice: {fbr_invoice_number}"
            )
            
            return {
                "fbr_invoice_number": fbr_invoice_number,
                "raw_response": response_data,
            }
            
        except requests.RequestException as e:
            logger.error(f"[POS Client] Network error: {e}")
            raise
        except POSAPIError:
            raise
        except Exception as e:
            logger.error(f"[POS Client] Unexpected error: {e}")
            raise POSAPIError(
                error_code="UNK",
                message=str(e),
                raw_response={}
            )

    def test_connection(self) -> dict:
        """
        Test FBR POS endpoint reachability and auth.

        Returns full raw FBR response so the caller can see exactly
        what FBR is saying. No assumptions about what status = good/bad.

        Returns:
            dict {
                "success": bool,
                "http_status": int,
                "fbr_response": str,       # raw response body
                "sent_headers": dict,      # what we sent (token masked)
                "sent_payload": dict,      # what we sent to FBR
                "message": str,
            }
        """
        import datetime

        env = "sandbox" if self.is_sandbox else "production"

        # Formatted Date without 'T' character
        current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        test_payload = {
            "InvoiceNumber": "",
            "POSID": int(self.pos_id),
            "USIN": "TST-CONN-CHECK-01",
            "DateTime": current_time,
            "BuyerName": "Walk-In Customer",
            "BuyerNTN": "0000000-0",
            "BuyerCNIC": "00000-0000000-0",
            "BuyerPhoneNumber": "03000000000",
            "TotalSaleValue": 1180.00,
            "TotalQuantity": 1.00,
            "TotalTaxCharged": 180.00,
            "Discount": 0.00,
            "FurtherTax": 0.00,
            "TotalBillAmount": 1180.00,
            "PaymentMode": 1,
            "RefInvoiceNumber": None,
            "InvoiceType": 1,
            "Items": [
                {
                    "ItemCode": "TEST-01",
                    "ItemName": "Connection Test Item",
                    "PCTCode": "00000000",
                    "Quantity": 1.00,
                    "TaxRate": 18.00,
                    "SaleValue": 1000.00,
                    "TotalAmount": 1180.00,
                    "TaxCharged": 180.00,
                    "Discount": 0.00,
                    "InvoiceType": 1
                }
            ]
        }

        headers = self._headers()
        # Mask token in diagnostic output (show first 8 chars only)
        token_val = headers.get("Authorization", "")
        masked_headers = {
            **headers,
            "Authorization": token_val[:15] + "..." if len(token_val) > 15 else token_val,
        }

        print("="*50)
        print(f"[POS Test] Sending to: {self.base_url}")
        print(f"[POS Test] Headers: {masked_headers}")
        print(f"[POS Test] Payload: {test_payload}")
        print("="*50)

        try:
            resp = requests.post(
                self.base_url,
                json=test_payload,
                headers=headers,
                timeout=15,
                verify=True,   # Attempt secure connection first to avoid warnings
            )

            # Try to parse JSON, fall back to raw text
            try:
                fbr_body = resp.json()
            except Exception:
                fbr_body = resp.text

            print(f"[POS Test] RECEIVED HTTP {resp.status_code}")
            print(f"[POS Test] FBR Body: {fbr_body}")
            print("="*50)

            if resp.status_code in (401, 403):
                # Try to parse WSO2-specific fault codes
                fault_code = None
                fault_msg = ""
                if isinstance(fbr_body, dict):
                    fault = fbr_body.get("fault", {})
                    fault_code = fault.get("code")
                    fault_msg = fault.get("message", "") + " — " + fault.get("description", "")

                # WSO2 code 900908 = "Resource forbidden" = WRONG ENDPOINT PATH
                # The token IS valid but the API subscription doesn't cover this URL.
                # This is NOT a bad token — it's a wrong endpoint.
                if fault_code == 900908:
                    return {
                        "success": False,
                        "environment": env,
                        "http_status": resp.status_code,
                        "fbr_response": fbr_body,
                        "sent_headers": masked_headers,
                        "sent_payload": test_payload,
                        "message": (
                            "❌ Token is VALID but ACCESS FORBIDDEN (900908). "
                            "This means your token is correct, but you don't have access to this specific endpoint. "
                            f"({fault_msg}) "
                            "Reasons: 1) You need FBR to whitelist your server's IP address. "
                            "2) You are using the Production URL but haven't been approved for go-live yet. "
                            "Try the other endpoint, or contact FBR to whitelist your IP."
                        ),
                    }

                # 900902 = Missing Credentials, 900901 = Invalid Credentials (real token problem)
                return {
                    "success": False,
                    "environment": env,
                    "http_status": resp.status_code,
                    "fbr_response": fbr_body,
                    "sent_headers": masked_headers,
                    "sent_payload": test_payload,
                    "message": (
                        f"FBR returned HTTP {resp.status_code}. "
                        f"FBR says: {fault_msg or fbr_body}. "
                        "Token may be expired or incorrect — reset it from the FBR portal."
                    ),
                }

            # Any other response (200, 400, 422…) = endpoint reachable, auth OK
            # FBR will reject the empty/dummy payload — that is expected.
            return {
                "success": True,
                "environment": env,
                "http_status": resp.status_code,
                "fbr_response": fbr_body,
                "sent_headers": masked_headers,
                "sent_payload": test_payload,
                "message": (
                    f"Connection OK! FBR endpoint reachable (HTTP {resp.status_code}). "
                    f"FBR response: {str(fbr_body)[:120]}"
                ),
            }

        except requests.exceptions.ConnectionError as e:
            msg = (
                f"Cannot reach {self.base_url}. "
                "Check internet / firewall. "
                "FBR may require your server IP to be whitelisted. "
                f"Detail: {e}"
            )
            logger.error(f"[POS Test] ConnectionError: {e}")
            return {
                "success": False,
                "environment": env,
                "http_status": None,
                "fbr_response": None,
                "sent_headers": masked_headers,
                "sent_payload": test_payload,
                "message": msg,
            }

        except requests.exceptions.Timeout:
            msg = f"Timed out after 15 s. FBR endpoint {self.base_url} may be down."
            logger.error(f"[POS Test] Timeout")
            return {
                "success": False,
                "environment": env,
                "http_status": None,
                "fbr_response": None,
                "sent_headers": masked_headers,
                "sent_payload": test_payload,
                "message": msg,
            }

        except Exception as e:
            logger.exception(f"[POS Test] Unexpected: {e}")
            return {
                "success": False,
                "environment": env,
                "http_status": None,
                "fbr_response": None,
                "sent_headers": masked_headers,
                "sent_payload": test_payload,
                "message": str(e),
            }
