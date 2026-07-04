# Login Pages - Testing Guide

## 📋 Overview

We've created a comprehensive dual login system with a white and teal color scheme:

1. **Login Choice Page** - Main landing page where users select login type
2. **Admin Login Page** - For administrators and platform staff
3. **Company Owner Login Page** - For business owners, managers, and staff

## 🎨 Color Scheme

- **Primary**: Teal (`teal-600`, `teal-700`) - #14b8a6
- **Background**: White/Light Teal (`teal-50`)
- **Text**: Dark Gray (`gray-900`)
- **Borders**: Light Gray/Teal border

## 📁 Files Created

```
src/pages/auth/
├── LoginChoicePage.vue          # Main login selection page
├── AdminLoginPage.vue           # Admin/Admin staff login
├── CompanyOwnerLoginPage.vue    # Owner/Manager/Cashier login
└── LoginPage.vue                # Redirects to LoginChoicePage (for backward compat)
```

## 🚀 How to Test

### Step 1: Install Dependencies & Start Dev Server

```bash
cd fbr_pos_frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Server will run on: **http://localhost:5173**

### Step 2: Test Login Flow

#### Flow 1: Admin Login
1. Go to http://localhost:5173
2. Should redirect to `/dashboard` (if not logged in) → then to `/login`
3. Click on **"Admin Portal"** button
4. See admin login form with:
   - Email input field with envelope icon
   - Password input field with show/hide toggle
   - "Sign In" button (teal color)
   - "Back to Login Selection" link
   - "Platform Administrator Access Only" footer

5. Try logging in with admin credentials:
   ```
   Email: admin@example.com
   Password: your_admin_password
   ```

6. **Expected Result**:
   - If credentials are valid and role is `admin` or `admin_staff`:
     - Redirect to `/dashboard`
     - AppLayout should show (with sidebar navigation)
   - If invalid credentials:
     - Show error message in red
   - If user role is not admin:
     - Show "Unauthorized: Admin access required" error
     - Auto logout

#### Flow 2: Company Login
1. Go to http://localhost:5173/login
2. Click on **"Company Login"** button
3. See company login form with:
   - Email input field with envelope icon
   - Password input field with show/hide toggle
   - **Remember this device** checkbox
   - "Sign In" button (teal color)
   - "Back to Login Selection" link
   - **Tip box** with helpful info
   - "FBR POS Platform · Powered by Digital Invoicing" footer

4. Try logging in with company credentials:
   ```
   Email: owner@company.com
   Password: your_password
   ```

5. **Expected Result**:
   - If credentials are valid and role is `owner`, `manager`, `cashier`, or `salesperson`:
     - Redirect to `/dashboard`
     - AppLayout should show (with sidebar navigation)
   - If invalid credentials:
     - Show error message in red
   - If user role is not company-related:
     - Show "Unauthorized: Company access required" error
     - Auto logout

### Step 3: Test UI Features

#### Admin Login Page
- ✅ Teal color scheme (header, buttons, borders)
- ✅ Envelope icon in email field
- ✅ Password show/hide toggle button
- ✅ Icons in buttons
- ✅ Responsive design (works on mobile)
- ✅ Loading spinner while submitting
- ✅ Error messages display correctly

#### Company Login Page
- ✅ All above features
- ✅ "Remember this device" checkbox
- ✅ Helpful tip box (blue background)
- ✅ Better footer message

#### Login Choice Page
- ✅ Two clear options: Admin Portal & Company Login
- ✅ Hover effects (border and shadow changes)
- ✅ Icons next to each option
- ✅ Clear descriptions for each login type
- ✅ Smooth transitions

### Step 4: Test Authentication Logic

#### Scenario 1: Valid Admin Login
```
Prerequisites:
- Django backend running on http://localhost:8000
- Admin user created in backend

Test:
1. Use admin email and password
2. Should successfully login
3. Token stored in localStorage
4. Redirected to dashboard
5. Refresh page → still logged in (token from localStorage)
```

#### Scenario 2: Valid Company User Login
```
Prerequisites:
- Django backend running on http://localhost:8000
- Company user (owner/manager/cashier) created in backend

Test:
1. Use company user email and password
2. Should successfully login
3. Token stored in localStorage
4. Redirected to dashboard
5. Refresh page → still logged in
```

#### Scenario 3: Invalid Credentials
```
Test:
1. Enter wrong email or password
2. See error message from backend
3. Not redirected
4. Can retry
```

#### Scenario 4: Wrong User Type
```
Prerequisites:
- Admin tries to login via Company Login page
- Company user tries to login via Admin Login page

Test:
1. Admin emails in company login → "Unauthorized: Company access required"
2. Company emails in admin login → "Unauthorized: Admin access required"
3. Both should auto-logout after error
```

### Step 5: Test Navigation After Login

After successful login, you should see:

**Sidebar Navigation Menu** with links to:
- 📊 Dashboard
- 🛒 Sales
- 📦 Products
- 🏷️ Categories
- 👥 Customers
- 💰 Cash Sessions
- ↩️ Returns
- 📄 Invoicing
- 📈 Reports
- 👤 Users
- 🎫 Subscriptions

**Top Right**: Logout button

## 🔧 Backend API Requirements

Make sure your Django backend is running and has these endpoints:

```
POST   /api/auth/login              # Required: returns { access, refresh }
GET    /api/auth/me                 # Required: returns current user data
POST   /api/auth/logout             # Required: logout endpoint
POST   /api/auth/refresh            # Required: refresh token endpoint
```

## 🚨 Troubleshooting

### Issue: "Cannot GET /api/auth/login" or CORS errors
**Solution**:
- Make sure Django backend is running on `http://localhost:8000`
- Check CORS settings in `config/settings.py`
- Should include `http://localhost:5173` in CORS allowed origins

### Issue: Login button disabled or slow
**Solution**:
- Check network tab in browser DevTools
- Ensure backend is responding
- Check browser console for errors

### Issue: Page stays on login after successful credentials
**Solution**:
- Check console for errors
- Make sure `/api/auth/me` endpoint exists
- Verify token is being stored in localStorage

### Issue: Can't see sidebar after login
**Solution**:
- Check browser console for component errors
- Verify AppLayout.vue is rendering
- Check that router is configured correctly

## 📱 Mobile Responsiveness

Test on mobile by:
1. Open DevTools (F12)
2. Click device toolbar (mobile icon)
3. Select iPhone 12 or similar
4. Test all login flows

**Features that should work on mobile**:
- ✅ Full form visibility
- ✅ Buttons are large enough to tap
- ✅ No horizontal scroll
- ✅ Icons render correctly
- ✅ Sidebar should collapse (or be accessible)

## 🔐 Security Notes

✅ **Currently Implemented**:
- JWT tokens stored in localStorage
- Bearer token added to all API requests
- Token refresh logic on 401 errors
- Auto logout on token expiry
- Role-based access control (admin vs company)

⚠️ **Not Yet Implemented** (for future):
- XSS protection
- CSRF tokens
- Secure HTTP-only cookies (better than localStorage)
- Password strength requirements
- Two-factor authentication
- Rate limiting on login attempts

## 📊 Component Structure

```
LoginChoicePage.vue
├── Header with logo and title
└── Two login option cards (Admin & Company)

AdminLoginPage.vue
├── Header (Admin Portal)
├── Form (email, password)
├── Error message display
└── Back link

CompanyOwnerLoginPage.vue
├── Header (Company Portal)
├── Form (email, password, remember me)
├── Tip box
├── Error message display
└── Back link
```

## 🎯 Next Steps After Login Works

1. ✅ Login pages created and tested
2. Next: Create dashboard with analytics
3. Create full POS sales module
4. Create product management pages
5. Create customer management pages
6. Create invoicing/FBR pages
7. Create reports
8. Create user management

## 📞 Support

If you encounter issues:
1. Check browser console (F12 → Console tab)
2. Check network requests (F12 → Network tab)
3. Verify Django backend is running
4. Check localStorage for tokens (F12 → Application tab)

---

**Happy Testing! 🎉**
