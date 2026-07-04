# Permission Management Feature - Implementation Plan

## Backend Summary 🎯

### Core Concepts:
1. **Permission** - Static catalogue (seeded once, never created at runtime)
   - Fields: `module`, `action`, `codename`, `label`, `description`, `is_active`
   - Example: `(module="fbr_di", action="view")` = "View FBR Digital Invoicing"

2. **UserPermission** - Junction table (user has permission)
   - Links `User` → `Permission`
   - Tracks `granted_by` (who assigned) and `granted_at`
   - Unique constraint: same user can't have same permission twice

3. **PermissionModule** - 20+ modules:
   - Sales: `sales_invoicing`, `fbr_di`, `customer_db`
   - Operations: `returns`, `cheque_bank_transfer`, `hardware_integration`
   - Inventory: `inventory`, `warehousing`
   - Reports: `basic_reports`, `advanced_reports`, `audit_logs`
   - Platform: `user_management`, `company_management`

4. **PermissionAction** - 6 atomic actions:
   - `VIEW`, `CREATE`, `EDIT`, `DELETE`, `EXPORT`, `APPROVE`

### API Endpoints:
```
GET    /api/permissions/
       → Returns all active permissions (admin/admin_staff only)
       → Response: [{ id, module, module_display, action, action_display, label, ... }]

GET    /api/user-permissions/{user_id}/panel/
       → Returns permission panel for a user (grouped by module)
       → Filters based on company's enabled modules
       → Response: [
           {
             "module": "fbr_di",
             "module_display": "FBR Digital Invoicing",
             "permissions": [
               { "id": 1, "action": "view", "label": "View FBR DI", "granted": true },
               { "id": 2, "action": "create", "label": "Create FBR DI", "granted": false },
               ...
             ]
           },
           ...
         ]

POST   /api/user-permissions/{user_id}/assign/
       → Replaces user's permissions with submitted list
       → Body: { "permission_ids": [1, 3, 7, 12] }
       → Idempotent: safe to call multiple times with same data
```

### Permission Rules:
- **Admin**: Bypasses all checks, no UserPermission rows needed
- **Admin Staff**: Can be granted platform permissions (USER_MANAGEMENT, COMPANY_MANAGEMENT)
- **Owner**: Auto-granted all permissions for enabled company modules (via signal)
- **Manager/Cashier/Salesperson**: Owner can assign permissions (capped at company modules)

---

## Frontend Architecture 🏗️

### New Files to Create:

#### 1. API Service Layer
**`src/apis/admin/permissionAPI.ts`**
```typescript
- getPermissions()                    // GET /api/permissions/
- getUserPermissionPanel(userId)      // GET /api/user-permissions/{userId}/panel/
- assignUserPermissions(userId, permissionIds)  // POST /api/user-permissions/{userId}/assign/
- listUserPermissions(userId)         // GET /api/user-permissions/{userId}/list/
```

#### 2. Types/Interfaces
**`src/types/index.ts`** (add to existing)
```typescript
interface Permission {
  id: number
  module: string
  module_display: string
  action: string
  action_display: string
  codename: string
  label: string
  description: string
  is_active: boolean
}

interface PermissionPanelGroup {
  module: string
  module_display: string
  permissions: {
    id: number
    action: string
    label: string
    codename: string
    granted: boolean
  }[]
}

interface UserPermission {
  id: number
  user: number
  permission: number
  permission_codename: string
  permission_label: string
  permission_module: string
  permission_module_display: string
  permission_action: string
  granted_by_email: string | null
  granted_at: string
}
```

#### 3. User Detail Page
**`src/pages/admin/UserDetailPage.vue`** (NEW)
- Shows user info: email, name, role, company, status
- Three buttons in header: **Edit** | **Delete** | **Manage Permissions**
- Info display with user avatar/badge
- Back button to return to users list

#### 4. User Edit Modal/Form
**`src/components/admin/EditUserModal.vue`** (NEW)
- Similar to AddUserModal but for editing
- Pre-fills form with current user data
- Disables role change (if not Admin)
- Fields: email, first_name, last_name, phone, password (optional)
- Save/Cancel buttons

#### 5. Delete Confirmation Modal
**`src/components/admin/DeleteUserConfirmModal.vue`** (NEW)
- Shows: "Are you sure you want to delete {user.email}?"
- Warning: This action cannot be undone
- Buttons: "Cancel" | "Delete"
- Loading state on delete

#### 6. Permissions Management Page
**`src/pages/admin/UserPermissionsPage.vue`** (NEW)
- Shows user info in header (breadcrumb: Users > {email} > Permissions)
- Permission groups displayed as **cards**
- Each card:
  - Header: Module name (e.g., "FBR Digital Invoicing")
  - Body: List of actions with checkboxes
    - [ ] View
    - [ ] Create
    - [x] Edit
    - [ ] Delete
    - [ ] Export
    - [ ] Approve
  - Footer buttons: "Select All" | "Select None"
- Bottom action buttons: "Save Permissions" | "Cancel"
- Loading/error states
- Toast notification on save success

#### 7. Store (Pinia)
**`src/stores/admin/permissionStore.ts`** (NEW)
```typescript
State:
- selectedPermissions: Set<number>
- availablePermissions: PermissionPanelGroup[]
- loading: boolean
- error: string

Actions:
- loadPermissionPanel(userId)
- togglePermission(permissionId)
- togglePermissionGroup(moduleKey)  // Select/deselect all in group
- savePermissions(userId)
- clearError()
```

#### 8. Router Updates
**`src/router/index.ts`** (UPDATE)
```typescript
New routes:
{
  path: 'users/:id',
  name: 'UserDetail',
  component: () => import('@/pages/admin/UserDetailPage.vue'),
  meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] }
},
{
  path: 'users/:id/permissions',
  name: 'UserPermissions',
  component: () => import('@/pages/admin/UserPermissionsPage.vue'),
  meta: { requiresAuth: true, requiredRole: ['admin', 'admin_staff'] }
}
```

---

## UI/UX Design 🎨

### Users List Page (Update)
Replace "Actions" column with clickable row:
```
┌─────────────────────────────────────────────────────────┐
│ Email              Full Name      Role          Status  │
├─────────────────────────────────────────────────────────┤
│ admin@gmail.com    -              Admin         Active  │ ← Click to go to detail
│ test@user.com      Test User      Admin Staff   Active  │
└─────────────────────────────────────────────────────────┘
```

### User Detail Page
```
┌─ Back Button
│
├─ User Header
│  ├─ Avatar (initials)
│  ├─ Email: admin@gmail.com
│  ├─ Name: Admin User
│  ├─ Role: [Admin Badge]
│  └─ Status: [Active Badge]
│
├─ Action Buttons: [Edit] [Delete] [Manage Permissions]
│
└─ User Info Section
   ├─ Full Name: Admin User
   ├─ Phone: +92 300 1234567
   ├─ Company: Acme Inc
   ├─ Role: Admin
   ├─ Status: Active
   ├─ Joined: Jun 26, 2026
   └─ Last Login: Jun 26, 2026 at 2:30 PM
```

### Permissions Management Page
```
┌─ Breadcrumb: Users > admin@gmail.com > Permissions
│
├─ Permission Cards (gridbox or list)
│
│  ┌─ FBR Digital Invoicing ─────────────────────┐
│  │                                              │
│  │ [✓] View           [✓] Create        [✗] Edit     │
│  │ [✗] Delete         [✗] Export        [✗] Approve  │
│  │                                              │
│  │ [Select All]  [Select None]                 │
│  └──────────────────────────────────────────────┘
│
│  ┌─ Inventory ──────────────────────────────────┐
│  │                                              │
│  │ [✓] View           [✗] Create        [✗] Edit     │
│  │ [✗] Delete         [✓] Export        [✗] Approve  │
│  │                                              │
│  │ [Select All]  [Select None]                 │
│  └──────────────────────────────────────────────┘
│
│  ... (more modules)
│
└─ Action Buttons: [Save Permissions] [Cancel]
```

---

## Implementation Sequence 📋

### Phase 1: API & Store
1. ✅ Create `permissionAPI.ts` with 4 endpoint methods
2. ✅ Create `permissionStore.ts` Pinia store
3. ✅ Add Permission types to `src/types/index.ts`

### Phase 2: User Detail & Edit Flow
1. ✅ Create `UserDetailPage.vue`
2. ✅ Create `EditUserModal.vue`
3. ✅ Create `DeleteUserConfirmModal.vue`
4. ✅ Update AdminUsersPage to make rows clickable
5. ✅ Add routes for `/admin/users/:id` and `/admin/users/:id/edit`

### Phase 3: Permissions UI
1. ✅ Create `UserPermissionsPage.vue` with permission cards
2. ✅ Create reusable `PermissionCard.vue` component
3. ✅ Add route for `/admin/users/:id/permissions`
4. ✅ Implement "Select All / Select None" functionality

### Phase 4: Integration & Testing
1. ✅ Test all flows end-to-end
2. ✅ Error handling and validation
3. ✅ Loading states and spinners
4. ✅ Toast notifications for feedback

---

## API Error Handling

All API responses use standard error format:
```json
{
  "detail": "Error message",
  "non_field_errors": ["Error 1", "Error 2"],
  "field_name": ["Field-specific error"]
}
```

---

## Notes 📝

- Permissions are **read-only** in terms of adding new permissions (admin does this via backend)
- Only **assignment** is managed (which permissions a user has)
- **Platform users** (Admin, Admin Staff) see different modules than **client users** (Manager, Cashier, etc.)
- **Company ceiling**: Client users can't be granted permissions their company doesn't have
- **Owner bypass**: Owners automatically get all permissions for their company's enabled modules
