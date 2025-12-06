# AntiGravity Attendance System - Multi-Portal Walkthrough

## Overview
The system has been successfully separated into three distinct portals, each with its own authentication, UI theme, and feature set.

## Portals

### 1. Admin Portal
-   **URL**: [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)
-   **Theme**: Dark / Professional
-   **Features**:
    -   Global Dashboard (Stats)
    -   Add Teachers (with Email)
    -   Add Students (with PRN & Semester)
    -   Add Subjects
    -   Manage System
-   **Login**: Username `admin` / Password `admin123`

### 2. Teacher Portal
-   **URL**: [http://127.0.0.1:5000/teacher/login](http://127.0.0.1:5000/teacher/login)
-   **Theme**: Teal / Clean
-   **Features**:
    -   Teacher Dashboard (Recent Sessions)
    -   Mark Attendance (Single-click Absent)
    -   View Class Stats
-   **Login**: Official Email (e.g., `teacher@siber.edu.in`) / Password

### 3. Student Portal
-   **URL**: [http://127.0.0.1:5000/student/login](http://127.0.0.1:5000/student/login)
-   **Theme**: Vibrant / Mobile-Friendly
-   **Features**:
    -   Personal Dashboard
    -   Attendance Analytics (Overall & Subject-wise)
    -   **Red Warning Banner** if attendance < 75%
    -   "Days to 75%" Calculator
-   **Login**: PRN (e.g., `2023001`) / Password

## Simulation Credentials
The system has been seeded with the following data:

### Admin
- **Login URL**: `/admin/login`
- **Username**: `admin`
- **Password**: `admin123`

### Teachers (9 Total)
- **Login URL**: `/teacher/login`
- **Login ID (Email)**: `teacher1@siber.edu.in` (up to `teacher9@siber.edu.in`)
- **Password**: `teacher1` (up to `teacher9`)

### Students (75 Total)
- **Login URL**: `/student/login`
- **Login ID (PRN)**: `2023001` (up to `2023075`)
- **Password**: `student1` (up to `student75`)
- **Note**: Do NOT use the username (`student1`) to log in. You must use the PRN.

## Setup Instructions
1.  **Run Simulation**: `python3 simulation_seed.py` (Already run)
    - Resets DB
    - Creates Admin, 9 Teachers, 75 Students
    - Simulates 90 days of attendance
2.  **Start Server**: `python3 run.py`
3.  **Access**: Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Technical Details
-   **Backend**: Flask with Blueprints (`admin_bp`, `teacher_bp`, `student_bp`).
-   **Auth**: Custom decorators (`@admin_required`, `@teacher_required`, `@student_required`) ensure strict role separation.
-   **Frontend**: Jinja2 templates with separate base layouts and CSS files for each role.
