from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from ..models import Student, AttendanceRecord, AttendanceSession, Subject, User
from functools import wraps
import math

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('You must be a student to access this page.')
            return redirect(url_for('student.login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.role == 'student':
        return redirect(url_for('student.dashboard'))
        
    if request.method == 'POST':
        prn = request.form.get('prn')
        password = request.form.get('password')
        
        student = Student.query.filter_by(prn=prn).first()
        if student:
            user = User.query.get(student.user_id)
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('student.dashboard'))
        
        flash('Invalid PRN or password')
            
    return render_template('student/login.html')

@student_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('student.login'))

@student_bp.route('/dashboard')
@student_required
def dashboard():
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    # Calculate Analytics
    records = AttendanceRecord.query.filter_by(student_id=student.id).all()
    total_lectures = len(records)
    attended_lectures = len([r for r in records if r.status == 'Present'])
    
    overall_percentage = (attended_lectures / total_lectures * 100) if total_lectures > 0 else 0
    
    # Calculate days required for 75%
    lectures_needed = 0
    if overall_percentage < 75:
        # Formula: (attended + x) / (total + x) = 0.75
        # attended + x = 0.75 * total + 0.75 * x
        # 0.25 * x = 0.75 * total - attended
        # x = (0.75 * total - attended) / 0.25
        # x = 3 * total - 4 * attended
        
        # Simplified:
        # target_attended = 0.75 * (total + x)
        # current_attended + x = 0.75 * total + 0.75 * x
        # 0.25x = 0.75 * total - current_attended
        # x = (3 * total - 4 * current_attended)
        
        # Wait, let's re-derive carefully.
        # We want (A + x) / (T + x) >= 0.75
        # A + x >= 0.75T + 0.75x
        # 0.25x >= 0.75T - A
        # x >= (0.75T - A) / 0.25
        # x >= 3T - 4A
        
        needed = (3 * total_lectures) - (4 * attended_lectures)
        lectures_needed = max(0, math.ceil(needed))

    # Subject-wise breakdown
    subject_stats = {}
    for record in records:
        subject_name = record.session.subject.name
        if subject_name not in subject_stats:
            subject_stats[subject_name] = {'total': 0, 'attended': 0}
        subject_stats[subject_name]['total'] += 1
        if record.status == 'Present':
            subject_stats[subject_name]['attended'] += 1
            
    # Calculate percentage for each subject
    for name, stats in subject_stats.items():
        if stats['total'] > 0:
            stats['percentage'] = round((stats['attended'] / stats['total']) * 100, 1)
        else:
            stats['percentage'] = 0
            
    return render_template('student/dashboard.html', 
                           student=student, 
                           overall_percentage=round(overall_percentage, 1),
                           lectures_needed=lectures_needed,
                           subject_stats=subject_stats)
