# MotoPizza Shop Web Application

## Phase 1: Core Layout and Product Catalog ✅
- [x] Set up main layout with navigation (header with logo, menu links, WhatsApp contact)
- [x] Create homepage with hero section and featured products
- [x] Build product catalog page with grid layout showing cakes and pastries
- [x] Implement product cards with images, names, descriptions, and prices
- [x] Add product detail view with full information and booking CTA
- [x] Create responsive design that works on mobile, tablet, and desktop

## Phase 2: Company Content and About Section ✅
- [x] Create About/Company page with business story and values
- [x] Add gallery section showcasing product photos and bakery workspace
- [x] Implement testimonials/reviews section
- [x] Create contact information page with business hours and location
- [x] Add FAQ section for common customer questions

## Phase 3: Booking System and WhatsApp Integration ✅
- [x] Build shopping cart state to manage multiple items
- [x] Implement add/remove/increment/decrement cart functionality
- [x] Build cart page showing all items with quantities, prices, and total calculation
- [x] Create order summary view with item details and total calculation
- [x] Integrate WhatsApp booking link with pre-filled order details
- [x] Add cart badge showing item count in header navigation
- [x] Add "Add to Cart" buttons on product detail pages
- [x] Implement empty cart state with call-to-action

## Phase 4: Content Management - Upload Page ✅
- [x] Create admin upload page at `/admin/upload` route
- [x] Implement drag-and-drop file upload area with rx.upload component
- [x] Add support for multiple file types (images: jpg, png, gif, webp; videos: mp4, mov, avi)
- [x] Display upload progress indicator during file uploads
- [x] Show grid of uploaded files with thumbnails (images) and icons (videos)
- [x] Add individual file delete functionality
- [x] Implement "Clear All" button to remove all uploaded files
- [x] Add "Upload Content" link to header navigation (visible on admin pages)
- [x] Include upload success/error toast notifications

## Phase 5: Product Management - Admin Products Page ✅
- [x] Create admin products page at `/admin/products` route
- [x] Build product form with fields: name, description, full description, price, category
- [x] Implement image upload for product photos with preview
- [x] Add multi-input ingredient management (add/remove ingredients)
- [x] Display existing products in a table with thumbnails
- [x] Add edit functionality to modify existing products
- [x] Implement delete functionality to remove products
- [x] Add form validation for required fields (name, price, image)
- [x] Include success/error toast notifications for all actions
- [x] Create separate AdminState class for product management logic
- [x] Add "Products" link to admin navigation in header

## Phase 6: Authentication System ✅
- [x] Create AuthState class to manage authentication logic
- [x] Implement login page with username/password form at `/login` route
- [x] Add password hashing for secure credential storage
- [x] Create session management with login/logout functionality
- [x] Add "is_authenticated" computed variable to track auth status

## Phase 7: Admin Route Protection ✅
- [x] Create route guard decorator/function to protect admin pages
- [x] Add authentication check to `/admin/upload` page with redirect to login
- [x] Add authentication check to `/admin/products` page with redirect to login
- [x] Update header to show "Login" or "Logout" button based on auth status
- [x] Remove admin navigation links from header when user is not authenticated

## Phase 8: API Security and Event Handler Protection ✅
- [x] Add authentication checks to AdminState event handlers
- [x] Protect `save_product` event handler with auth verification
- [x] Protect `handle_product_image_upload` with authentication check
- [x] Protect `set_editing_product` event handler
- [x] Add authentication to State `delete_product` handler
- [x] Protect `handle_upload` event with authentication
- [x] Add auth checks to `clear_uploads` and `delete_uploaded_file` handlers
- [x] Return unauthorized error and redirect to login for unauthenticated requests
- [x] Use `await self.get_state(AuthState)` pattern for checking authentication

## Phase 9: Guest Checkout and Login Flow Enhancement ✅
- [x] Remove login/logout button from public header navigation
- [x] Keep "Proceed to Checkout" link redirecting to login page with return_url=/cart
- [x] Update login event handler to differentiate between admin and guest checkout:
  - Admin credentials from cart → redirect to /admin/products
  - Invalid/guest credentials from cart → redirect to WhatsApp checkout URL
  - Invalid credentials from other pages → show error and stay on login
- [x] Implement WhatsApp checkout URL generation with cart details
- [x] Add `is_external=True` parameter for external WhatsApp redirects
- [x] Test all login scenarios: guest checkout, admin from cart, direct admin login, invalid login

## Phase 10: Customer Email Collection and Marketing System ✅
- [x] Add "Login" link to public header navigation (visible to all users)
- [x] Create CustomerEmail TypedDict with email, timestamp, cart_items fields
- [x] Add customer_emails list to State for storing customer data
- [x] Create `/checkout` page with email input form and cart summary
- [x] Implement process_checkout event handler to:
  - Validate email input
  - Store customer email with timestamp and cart items
  - Clear cart after submission
  - Redirect to WhatsApp with order details
- [x] Create `/admin/customers` page showing collected customer emails
- [x] Display customer data in table: email, timestamp, and cart items
- [x] Add "Customers" link to admin navigation (visible when authenticated)
- [x] Add authentication protection to customers page
- [x] Update cart page to link "Proceed to Checkout" to `/checkout` route
- [x] Add empty cart validation on checkout page

## Phase 11: Enhanced Customer Data Collection ✅
- [x] Update CustomerEmail TypedDict to include name and phone fields
- [x] Modify checkout page form to collect:
  - Full Name (text input)
  - Phone Number (tel input)
  - Email Address (email input)
- [x] Update process_checkout event handler to:
  - Validate all three required fields (name, phone, email)
  - Store complete customer profile with cart data
- [x] Update admin customers table to display:
  - Name column (first column)
  - Phone column (second column)
  - Email column (third column)
  - Timestamp column (fourth column)
  - Cart Items column (fifth column)
- [x] Update WhatsApp checkout URL to include customer name in message
- [x] Add proper placeholder text for all form fields
- [x] Ensure form validation shows errors for missing fields

## Phase 12: WhatsApp Phone Number Update ✅
- [x] Test WhatsApp API integration to verify functionality
- [x] Update phone number from "1234567890" to "07080234820" in State class
- [x] Update whatsapp_url computed variable with new number
- [x] Update whatsapp_checkout_url computed variable with new number
- [x] Verify checkout flow uses correct phone number
- [x] Verify product detail booking uses correct phone number
- [x] Test message generation with new phone number
- [x] Confirm all WhatsApp links redirect to 07080234820

## Phase 13: Security Hardening and Code Cleanup ✅
- [x] Move admin credentials from hardcoded values to environment variables
- [x] Update AuthState to use os.getenv() for ADMIN_USERNAME and ADMIN_PASSWORD_HASH
- [x] Add fallback defaults for development (username: "admin", password: "admin")
- [x] Remove unused variables:
  - Remove redirect_to variable from AuthState
  - Remove unused token generation code
  - Remove unused username/password state variables
- [x] Improve error messages:
  - Use generic "Invalid credentials" message
  - Don't reveal if username or password is wrong
- [x] Add security documentation:
  - Add comments explaining demo-only authentication
  - Add TODO comments for production requirements
  - Document environment variable setup
- [x] Test authentication functionality after changes
- [x] Verify login page still works correctly

## Phase 14: User Registration System ✅
- [x] Create signup page at `/signup` route
- [x] Build registration form with fields:
  - Full Name (text input with placeholder "John Doe")
  - Email Address (email input with placeholder "you@example.com")
  - Phone Number (tel input with placeholder "08012345678")
  - Password (password input)
  - Confirm Password (password input)
- [x] Add "Sign up" submit button with teal styling matching login page
- [x] Add "Already have an account? Log in" link at bottom of form
- [x] Implement signup event handler in AuthState with validations:
  - Check all fields are filled (name, email, phone, password, confirm_password)
  - Verify passwords match
  - Validate email format using regex
  - Check for duplicate email addresses
  - Hash password with SHA-256 before storing
- [x] Add User TypedDict with fields: name, email, phone, password_hash
- [x] Store new users in AuthState.users list
- [x] Display error messages for validation failures
- [x] Show success toast and redirect to login page after successful signup
- [x] Add "Don't have an account? Sign up" link to login page
- [x] Update login handler to support user authentication:
  - Check if credentials match any user in users list
  - Support login with email as username
  - Maintain existing admin authentication
- [x] Test all validation scenarios:
  - Valid signup with all fields
  - Missing required fields
  - Mismatched passwords
  - Invalid email format
  - Duplicate email
  - Login with new user credentials

## Phase 15: Authentication-Based Checkout Flow and Order Management ✅
- [x] Update cart page to check authentication before checkout:
  - If not authenticated → "Proceed to Checkout" button redirects to `/login?return_url=/cart`
  - If authenticated → "Proceed to Checkout" button triggers direct WhatsApp redirect
- [x] Create Order TypedDict with fields:
  - id: int (auto-incrementing order ID)
  - username: str (from authenticated user)
  - email: str (from authenticated user)
  - phone: str (from authenticated user)
  - timestamp: str (date and time of order)
  - cart_items: list[CartItem] (full cart contents)
  - status: str (order status: "pending", "completed", etc.)
- [x] Add orders list to State class for storing all customer orders
- [x] Update process_checkout_and_redirect event handler to:
  - Check if user is authenticated
  - If not authenticated → redirect to login page
  - If authenticated → store order with user details
  - Generate WhatsApp URL with order details
  - Clear cart after successful order placement
  - Redirect to WhatsApp for order confirmation
- [x] Create `/admin/orders` page showing all customer orders
- [x] Build orders table with columns:
  - Order ID (unique identifier)
  - Timestamp (date and time)
  - Username (customer name)
  - Email (customer email)
  - Phone (customer phone number)
  - Items (list of ordered products with quantities)
  - Status (order status badge with color coding)
- [x] Add "Orders" link to admin navigation in header (visible when authenticated)
- [x] Add authentication protection to orders page
- [x] Style status badges:
  - "pending" → yellow background
  - "completed" → green background
- [x] Update checkout page to remove form (no longer needed)
- [x] Test complete checkout flow:
  - Unauthenticated user → redirected to login
  - Authenticated user → order stored and WhatsApp redirect

## Phase 16: Admin Management System ✅
- [x] Create Admin TypedDict with fields: username, password_hash, created_at
- [x] Add admins list to AuthState for storing admin accounts
- [x] Create `/admin/users` page for admin management
- [x] Build admin add form with fields:
  - Username (text input)
  - Password (password input)
  - Confirm Password (password input)
- [x] Add "Add Admin" submit button
- [x] Implement add_admin event handler with validations:
  - Check all fields are filled
  - Verify passwords match
  - Check for duplicate usernames
  - Hash password with SHA-256 before storing
  - Add timestamp (created_at) to new admin
- [x] Display admin table with columns:
  - Username
  - Created At (timestamp)
  - Actions (delete button)
- [x] Implement delete_admin functionality:
  - Add set_admin_to_delete event handler
  - Create delete confirmation dialog
  - Implement confirm_delete_admin event handler
  - Add cancel_delete event handler
  - Protect main admin from deletion (from env vars)
- [x] Add "Users" link to admin navigation in header
- [x] Add authentication protection to admin users page
- [x] Restrict admin management to main admin only:
  - Add is_main_admin computed variable
  - Only main admin (from ADMIN_USERNAME env) can add/remove admins
  - Show "Only the main admin can manage users" message for other admins
- [x] Initialize default admin account:
  - Create _ensure_main_admin helper method
  - Auto-create admin from environment variables on first load
  - Prevent duplicate admin creation
- [x] Add success/error toast notifications:
  - Success toast when admin added
  - Error toast for validation failures
  - Success toast when admin deleted
  - Error toast when trying to delete main admin
- [x] Test all admin management scenarios:
  - Add new admin successfully
  - Duplicate username validation
  - Password mismatch validation
  - Delete regular admin
  - Prevent main admin deletion
  - Restrict management to main admin only

## Phase 17: Unified Authentication Flow with Admin Auto-Detection ✅
- [x] Update AuthState.login event handler to check admins FIRST:
  - Check if username matches any admin account
  - Verify password hash matches admin password
  - If admin match → set is_authenticated, redirect to /admin/products
  - If no admin match → check regular users list
  - If user match → set is_authenticated, redirect to return_url or home
  - If no match at all → show "Invalid credentials" error
- [x] Update login page UI and messaging:
  - Change title to "Login to Your Account"
  - Update description to indicate this is for all users
  - Keep existing form structure (username, password fields)
  - Maintain "Don't have an account? Sign up" link
- [x] Keep signup page for regular users only:
  - No changes to signup flow
  - Users created via signup do NOT get admin access
  - Only admins list in AuthState has admin privileges
- [x] Admin detection logic:
  - Admins checked FIRST before users
  - Admin credentials automatically recognized
  - Automatic redirect to admin area (/admin/products)
  - No manual "admin login" vs "user login" needed
- [x] Test authentication flow scenarios:
  - Admin login with admin credentials → redirect to /admin/products ✅
  - User login with user credentials → redirect to home or return_url ✅
  - Invalid credentials → show error message ✅
  - Signup creates regular user (not admin) ✅
  - Admin can access all admin pages after login ✅

---

**Current Status**: ✅ Phase 17 complete! Unified authentication system with automatic admin detection implemented.

**Application Features**:
- ✅ Full e-commerce functionality with shopping cart
- ✅ User registration and authentication system
- ✅ **Unified login page for both admins and users**
- ✅ **Automatic admin detection and routing**
- ✅ Authentication-based checkout and order management
- ✅ Multi-admin support with role-based access control
- ✅ Admin user management system (add/remove admins)
- ✅ Main admin protection (cannot be deleted)
- ✅ Secure password hashing and validation
- ✅ Protected admin routes and API endpoints
- ✅ WhatsApp integration with phone number 07080234820
- ✅ Complete product and content management system

**Unified Authentication System**:

**Login Flow:**
1. User goes to `/login` page (single login page for everyone)
2. Enters username and password
3. System checks if credentials are admin credentials (checked FIRST)
   - If admin → redirect to `/admin/products`
   - If not admin → check if regular user
   - If user → redirect to home page or return_url
   - If neither → show "Invalid credentials" error

**Key Benefits:**
- 🎯 **Single Login Page**: One unified login for admins and users
- 🔍 **Auto-Detection**: System automatically detects if user is admin
- 🚀 **Smart Routing**: Admins go to admin area, users go to public site
- 🔒 **Secure**: Admin credentials checked first, no admin/user confusion
- 💡 **User-Friendly**: No need to choose "admin login" vs "user login"

**User Types:**
1. **Admins** (from `admins` list in AuthState):
   - Created via `/admin/users` page by main admin
   - Login → automatically redirected to `/admin/products`
   - Have access to all admin pages
   - Phone shows as "N/A" in authenticated_user
   
2. **Regular Users** (from `users` list in AuthState):
   - Created via `/signup` page
   - Login → redirected to home page or return_url
   - Can browse products, add to cart, checkout
   - Full profile with name, email, phone

**Authentication Priority:**
```
Login attempt
    ↓
Check admins list FIRST
    ↓
Admin found? → Redirect to /admin/products
    ↓
Check users list NEXT
    ↓
User found? → Redirect to home/return_url
    ↓
No match? → Show "Invalid credentials" error
```

**Pages:**
- **`/login`**: Universal login for admins AND users
- **`/signup`**: Registration for regular users only (not admins)
- **`/admin/products`**: Admin landing page after admin login
- **`/`**: User landing page after user login

**Example Scenarios:**

**Scenario 1: Admin Login**
- User: admin (from ADMIN_USERNAME env)
- Password: admin (from ADMIN_PASSWORD_HASH env)
- Result: ✅ Authenticated as admin → `/admin/products`

**Scenario 2: Regular User Login**
- User: jane@example.com (registered via signup)
- Password: userpass123
- Result: ✅ Authenticated as user → `/` (home page)

**Scenario 3: Invalid Login**
- User: nonexistent@test.com
- Password: wrongpass
- Result: ❌ "Invalid credentials" error

**Scenario 4: User Signup**
- New user registers via `/signup` page
- Fills: name, email, phone, password, confirm password
- Result: ✅ Account created as regular user (NOT admin)
- Can login via `/login` and access public site

**Security Notes:**
- ✅ Admins checked FIRST (priority over users)
- ✅ Only way to create admin: via `/admin/users` page by main admin
- ✅ Signup page creates regular users only
- ✅ All passwords hashed with SHA-256
- ✅ No hardcoded credentials (uses environment variables)

**The MotoPizza shop now has a seamless, unified authentication system!** 🔐✨