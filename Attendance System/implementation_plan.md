# Implementation Plan - Admin Delete & System Reset

## Goal
Enable Admin to view and delete Teachers and Students. Reset the system data to ensure a clean slate and full functionality.

## Proposed Changes

### Database Models
#### [MODIFY] [app/models.py](file:///Users/kunalkapoor/AntiGravity/app/models.py)
-   Add `cascade="all, delete-orphan"` to `User` relationships (`teacher_profile`, `student_profile`).
-   Add `cascade="all, delete-orphan"` to `AttendanceSession` records.
-   Add `cascade="all, delete-orphan"` to `Student` records (for `AttendanceRecord`).

### Admin Backend
#### [MODIFY] [app/routes/admin.py](file:///Users/kunalkapoor/AntiGravity/app/routes/admin.py)
-   Add route `/users/manage` to list all users (Teachers/Students).
-   Add route `/users/delete/<int:user_id>` to delete a user.
-   Add route `/subjects/manage` to list and delete subjects.
-   Add route `/subjects/delete/<int:subject_id>` to delete a subject.

### Admin Frontend
#### [NEW] [app/templates/admin/manage_users.html](file:///Users/kunalkapoor/AntiGravity/app/templates/admin/manage_users.html)
-   Table listing all users with "Delete" button.
-   Tabs or sections for Teachers vs Students.

#### [NEW] [app/templates/admin/manage_subjects.html](file:///Users/kunalkapoor/AntiGravity/app/templates/admin/manage_subjects.html)
-   Table listing all subjects with "Delete" button.

#### [MODIFY] [app/templates/admin/dashboard.html](file:///Users/kunalkapoor/AntiGravity/app/templates/admin/dashboard.html)
-   Add links to "Manage Teachers", "Manage Students", "Manage Subjects".

### System Reset
-   **Action**: Delete `instance/db.sqlite3`.
-   **Action**: Run `seed_data.py` to recreate fresh data.

## Verification Plan
### Manual Verification
1.  **Reset**: Confirm database is empty (except seed data).
2.  **Admin**:
    -   Login as Admin.
    -   Go to "Manage Teachers".
    -   Delete "Demo Teacher".
    -   Verify Teacher is gone from list and DB.
    -   Go to "Manage Students".
    -   Delete "Demo Student".
    -   Verify Student is gone.
