from rest_framework import viewsets
from common.permissions import IsOwnerOrAdmin
from companies.mixins import AuditLogMixin
from .models import (
    AcademicSession, grade, section, subject, ClassSubjectAssignment,
    guardian, Student, StudentGuardianAssignment, Staff, Enrollment, Attendance,
    FeeHead, FeeStructure, FeeStructureItem, StudentFeeConcession,
    ExamType, Exam, ExamSubjectSchedule, StudentExamResult,
    FeeInvoice, FeeInvoiceItem, FeePayment
)
from .serializers import (
    AcademicSessionSerializer, GradeSerializer, SectionSerializer, SubjectSerializer,
    ClassSubjectAssignmentSerializer, GuardianSerializer, StudentSerializer,
    StudentGuardianAssignmentSerializer, StaffSerializer, EnrollmentSerializer,
    AttendanceSerializer, FeeHeadSerializer, FeeStructureSerializer,
    FeeStructureItemSerializer, StudentFeeConcessionSerializer,
    ExamTypeSerializer, ExamSerializer, ExamSubjectScheduleSerializer, StudentExamResultSerializer,
    FeeInvoiceSerializer, FeeInvoiceItemSerializer, FeePaymentSerializer
)

class BaseSchoolViewSet(AuditLogMixin, viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, 'swagger_fake_view', False):
            return qs.none()
        
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
            
        if user.is_platform_admin:
            return qs
            
        company = user.company
        if not company:
            return qs.none()
            
        # Try to dynamically filter based on model fields
        model_fields = [f.name for f in self.serializer_class.Meta.model._meta.get_fields()]
        
        if 'tennant_id' in model_fields:
            return qs.filter(tennant_id=company)
        elif 'company_id' in model_fields:
            return qs.filter(company_id=company)
            
        # For nested models without direct company FK
        model = self.serializer_class.Meta.model
        if model == section:
            return qs.filter(grade_id__tennant_id=company)
        elif model == ClassSubjectAssignment:
            return qs.filter(section_id__grade_id__tennant_id=company)
        elif model == StudentGuardianAssignment:
            return qs.filter(student_id__tennant_id=company)
        elif model == Enrollment:
            return qs.filter(student_id__tennant_id=company)
        elif model == Attendance:
            return qs.filter(student_id__tennant_id=company)
        elif model == FeeStructureItem:
            return qs.filter(fee_structure_id__tennant_id=company)
        elif model == StudentFeeConcession:
            return qs.filter(student_id__tennant_id=company)
        elif model == Exam:
            return qs.filter(exam_type_id__company_id=company)
        elif model == ExamSubjectSchedule:
            return qs.filter(exam_id__exam_type_id__company_id=company)
        elif model == StudentExamResult:
            return qs.filter(enrollment_id__student_id__tennant_id=company)
        elif model == FeeInvoice:
            return qs.filter(student_id__tennant_id=company)
        elif model == FeeInvoiceItem:
            return qs.filter(fee_invoice_id__student_id__tennant_id=company)
        elif model == FeePayment:
            return qs.filter(fee_invoice_id__student_id__tennant_id=company)
            
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_platform_admin:
            serializer.save()
            self.log_audit_action("create", serializer.instance)
            return
            
        company = user.company
        model_fields = [f.name for f in self.serializer_class.Meta.model._meta.get_fields()]
        
        # Enforce strict data isolation for any related fields passed in
        from rest_framework.exceptions import PermissionDenied
        for field, obj in serializer.validated_data.items():
            if hasattr(obj, 'tennant_id') and obj.tennant_id != company:
                raise PermissionDenied(f"Security error: Cannot link to {field} of another school.")
            if hasattr(obj, 'company_id') and obj.company_id != company:
                raise PermissionDenied(f"Security error: Cannot link to {field} of another school.")
            if hasattr(obj, 'student_id') and hasattr(obj.student_id, 'tennant_id') and obj.student_id.tennant_id != company:
                raise PermissionDenied(f"Security error: Cannot link to {field} of another school.")

        kwargs = {}
        if 'tennant_id' in model_fields:
            kwargs['tennant_id'] = company
        elif 'company_id' in model_fields:
            kwargs['company_id'] = company
            
        serializer.save(**kwargs)
        self.log_audit_action("create", serializer.instance)

    def perform_update(self, serializer):
        user = self.request.user
        if not user.is_platform_admin:
            company = user.company
            from rest_framework.exceptions import PermissionDenied
            for field, obj in serializer.validated_data.items():
                if hasattr(obj, 'tennant_id') and obj.tennant_id != company:
                    raise PermissionDenied(f"Security error: Cannot link to {field} of another school.")
                if hasattr(obj, 'company_id') and obj.company_id != company:
                    raise PermissionDenied(f"Security error: Cannot link to {field} of another school.")
                if hasattr(obj, 'student_id') and hasattr(obj.student_id, 'tennant_id') and obj.student_id.tennant_id != company:
                    raise PermissionDenied(f"Security error: Cannot link to {field} of another school.")
                    
        serializer.save()
        self.log_audit_action("update", serializer.instance)

class AcademicSessionViewSet(BaseSchoolViewSet):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer

class GradeViewSet(BaseSchoolViewSet):
    queryset = grade.objects.all()
    serializer_class = GradeSerializer

class SectionViewSet(BaseSchoolViewSet):
    queryset = section.objects.all()
    serializer_class = SectionSerializer

class SubjectViewSet(BaseSchoolViewSet):
    queryset = subject.objects.all()
    serializer_class = SubjectSerializer

class ClassSubjectAssignmentViewSet(BaseSchoolViewSet):
    queryset = ClassSubjectAssignment.objects.all()
    serializer_class = ClassSubjectAssignmentSerializer

class GuardianViewSet(BaseSchoolViewSet):
    queryset = guardian.objects.all()
    serializer_class = GuardianSerializer

class StudentViewSet(BaseSchoolViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentGuardianAssignmentViewSet(BaseSchoolViewSet):
    queryset = StudentGuardianAssignment.objects.all()
    serializer_class = StudentGuardianAssignmentSerializer

class StaffViewSet(BaseSchoolViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class EnrollmentViewSet(BaseSchoolViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class AttendanceViewSet(BaseSchoolViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class FeeHeadViewSet(BaseSchoolViewSet):
    queryset = FeeHead.objects.all()
    serializer_class = FeeHeadSerializer

class FeeStructureViewSet(BaseSchoolViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer

class FeeStructureItemViewSet(BaseSchoolViewSet):
    queryset = FeeStructureItem.objects.all()
    serializer_class = FeeStructureItemSerializer

class StudentFeeConcessionViewSet(BaseSchoolViewSet):
    queryset = StudentFeeConcession.objects.all()
    serializer_class = StudentFeeConcessionSerializer

class ExamTypeViewSet(BaseSchoolViewSet):
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer

class ExamViewSet(BaseSchoolViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamSubjectScheduleViewSet(BaseSchoolViewSet):
    queryset = ExamSubjectSchedule.objects.all()
    serializer_class = ExamSubjectScheduleSerializer

class StudentExamResultViewSet(BaseSchoolViewSet):
    queryset = StudentExamResult.objects.all()
    serializer_class = StudentExamResultSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from pos.models import Sale, SaleLine, Product, Customer, SaleStatus, FBRSubmissionStatus
from digital_invoicing.tasks import submit_invoice_to_fbr

class FeeInvoiceViewSet(BaseSchoolViewSet):
    queryset = FeeInvoice.objects.all()
    serializer_class = FeeInvoiceSerializer

    @action(detail=True, methods=['post'], url_path='generate-fbr')
    def generate_fbr(self, request, pk=None):
        fee_invoice = self.get_object()
        company = fee_invoice.student_id.tennant_id

        if fee_invoice.core_invoice_id:
            return Response({"error": "FBR Invoice already generated for this fee voucher."}, status=400)

        student = fee_invoice.student_id
        guardian_cnic = None
        if float(fee_invoice.total_payable_amount) >= 20000:
            primary_guardian_assignment = StudentGuardianAssignment.objects.filter(
                student_id=student, is_primary_billing_contact=True
            ).select_related('guardian_id').first()
            
            if primary_guardian_assignment and primary_guardian_assignment.guardian_id.cnic:
                guardian_cnic = primary_guardian_assignment.guardian_id.cnic
            elif fee_invoice.guardian_id and fee_invoice.guardian_id.cnic:
                guardian_cnic = fee_invoice.guardian_id.cnic
            
            if not guardian_cnic:
                return Response({
                    "error": "FBR requires a guardian CNIC for invoices of PKR 20,000 or more. Please link a guardian with a valid CNIC."
                }, status=400)

        with transaction.atomic():
            # 1. Calculate Fiscal Year boundaries
            today = timezone.now().date()
            if today.month >= 7:
                fy_start = today.replace(month=7, day=1)
                fy_end = today.replace(year=today.year + 1, month=6, day=30)
            else:
                fy_start = today.replace(year=today.year - 1, month=7, day=1)
                fy_end = today.replace(month=6, day=30)

            # 2. Calculate Total Fees Billed This Fiscal Year (excluding current)
            from django.db.models import Sum
            previous_billed = FeeInvoice.objects.filter(
                student_id=fee_invoice.student_id,
                invoice_date__range=(fy_start, fy_end),
                core_invoice_id__isnull=False  # Only count generated ones
            ).aggregate(total=Sum('total_amount'))['total'] or 0

            current_amount = fee_invoice.total_amount
            apply_236i_tax = (float(previous_billed) + float(current_amount)) > 200000

            # 3. Get or Create a dummy POS Customer for the Guardian/Student
            cnic = guardian_cnic or student.cnic or "0000000000000"
            customer_name = student.fullname
            if guardian_cnic and primary_guardian_assignment:
                customer_name = primary_guardian_assignment.guardian_id.fullname
            elif guardian_cnic and fee_invoice.guardian_id:
                customer_name = fee_invoice.guardian_id.fullname
                
            customer, _ = Customer.objects.get_or_create(
                company=company,
                ntn_cnic=cnic,
                defaults={
                    "name": customer_name,
                    "phone": student.phone_number or "00000000000",
                    "registration_type": "Unregistered",
                }
            )

            # 4. Get or Create a dummy School Fee Product
            fee_product, _ = Product.objects.get_or_create(
                company=company,
                name="School Fee Item",
                defaults={
                    "selling_price": 0,
                    "fbr_sale_type": "Services",
                    "unit_of_measure": "Nos",
                    "track_inventory": False,
                    "is_active": True,
                }
            )

            # 5. Create the POS Sale
            sale = Sale.objects.create(
                company=company,
                user=request.user if request.user.is_authenticated and not request.user.is_platform_admin else company.owner,
                customer=customer,
                status=SaleStatus.COMPLETED,
                fbr_submission_status=FBRSubmissionStatus.PENDING,
                completed_at=timezone.now(),
            )

            # 6. Map FeeInvoiceItems to SaleLines
            total_sale_amount = 0
            total_sale_tax = 0

            for item in fee_invoice.items.all():
                is_tuition = item.fee_head_id and "tuition" in item.fee_head_id.name.lower()
                tax_rate = 5.0 if (apply_236i_tax and is_tuition) else 0.0
                
                # Update the FeeInvoiceItem tax for record keeping
                item.tax_rate = tax_rate
                item.tax_amount = (float(item.total_amount) * tax_rate) / 100.0
                item.save(update_fields=['tax_rate', 'tax_amount'])

                line_val_excl = float(item.total_amount)
                line_tax = float(item.tax_amount)
                
                pct_code = item.pct_code
                if not pct_code and item.fee_head_id:
                    head_name = item.fee_head_id.name.lower()
                    if "tuition" in head_name or "admission" in head_name:
                        pct_code = "9992.1000"
                    elif "library" in head_name:
                        pct_code = "9992.2000"
                    elif "transport" in head_name or "van" in head_name:
                        pct_code = "9994.1100"
                    else:
                        pct_code = "9901.0000"
                if not pct_code:
                    pct_code = "9901.0000"
                
                SaleLine.objects.create(
                    sale=sale,
                    product=fee_product,
                    product_name=item.description or "School Fee",
                    hs_code=pct_code,
                    unit_of_measure="Nos",
                    fbr_sale_type="Services",
                    tax_rate_percent=str(tax_rate),
                    quantity=1.0,
                    unit_price=line_val_excl,
                    discount_amount=item.discount_amount,
                    value_excl_tax=line_val_excl,
                    sales_tax_applicable=line_tax,
                    line_total=line_val_excl + line_tax
                )
                total_sale_amount += (line_val_excl + line_tax)
                total_sale_tax += line_tax

            # 7. Add 1 Rupee FBR POS Service Fee (PCT 9902.0000)
            SaleLine.objects.create(
                sale=sale,
                product=fee_product,
                product_name="FBR POS Service Fee",
                hs_code="9902.0000",
                unit_of_measure="Nos",
                fbr_sale_type="Services",
                tax_rate_percent="0",
                quantity=1.0,
                unit_price=1.00,
                discount_amount=0,
                value_excl_tax=1.00,
                sales_tax_applicable=0,
                line_total=1.00
            )
            total_sale_amount += 1.00

            # 8. Update Sale Totals
            sale.subtotal = total_sale_amount - total_sale_tax
            sale.total_tax = total_sale_tax
            sale.total_amount = total_sale_amount
            sale.amount_paid = total_sale_amount
            sale.save(update_fields=['subtotal', 'total_tax', 'total_amount', 'amount_paid'])

            # 9. Link Back to FeeInvoice
            fee_invoice.core_invoice_id = sale
            fee_invoice.invoice_status_fbr = 'sent_to_fbr'
            fee_invoice.save(update_fields=['core_invoice_id', 'invoice_status_fbr'])

        # 10. Fire Celery Task to Submit to FBR
        submit_invoice_to_fbr.delay(sale.id)

        return Response({
            "message": "FBR Invoice generation triggered successfully.",
            "core_invoice_id": sale.id
        })

class FeeInvoiceItemViewSet(BaseSchoolViewSet):
    queryset = FeeInvoiceItem.objects.all()
    serializer_class = FeeInvoiceItemSerializer

class FeePaymentViewSet(BaseSchoolViewSet):
    queryset = FeePayment.objects.all()
    serializer_class = FeePaymentSerializer
