from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from ..models import db, Subject, Student, AttendanceSession, AttendanceRecord, Teacher, User
from functools import wraps

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            flash('You must be a teacher to access this page.')
            return redirect(url_for('teacher.login'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.role == 'teacher':
        return redirect(url_for('teacher.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find teacher by email
        teacher = Teacher.query.filter_by(email=email).first()
        if teacher:
            user = User.query.get(teacher.user_id)
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('teacher.dashboard'))
        
        flash('Invalid email or password')
            
    return render_template('teacher/login.html')

@teacher_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('teacher.login'))

@teacher_bp.route('/dashboard')
@teacher_required
def dashboard():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    # In a real app, we would filter subjects assigned to this teacher
    subjects = Subject.query.all() 
    
    # Get recent sessions
    recent_sessions = AttendanceSession.query.filter_by(teacher_id=teacher.id).order_by(AttendanceSession.created_at.desc()).limit(5).all()
    
    return render_template('teacher/dashboard.html', teacher=teacher, subjects=subjects, recent_sessions=recent_sessions)

@teacher_bp.route('/mark_attendance', methods=['GET', 'POST'])
@teacher_required
def mark_attendance():
    if request.method == 'POST':
        subject_id = request.form.get('subject')
        absent_student_ids = request.form.getlist('absent_students')
        
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        session = AttendanceSession(teacher_id=teacher.id, subject_id=subject_id)
        db.session.add(session)
        db.session.commit()
        
        subject = Subject.query.get(subject_id)
        all_students = Student.query.filter_by(semester=subject.semester).all()
        
        count_present = 0
        count_absent = 0
        
        for student in all_students:
            status = 'Absent' if str(student.id) in absent_student_ids else 'Present'
            record = AttendanceRecord(session_id=session.id, student_id=student.id, status=status)
            db.session.add(record)
            
            if status == 'Present':
                count_present += 1
            else:
                count_absent += 1
            
        db.session.commit()
        flash(f'Attendance marked: {count_present} Present, {count_absent} Absent')
        return redirect(url_for('teacher.dashboard'))
        
    subjects = Subject.query.all()
    return render_template('teacher/mark_attendance.html', subjects=subjects)

@teacher_bp.route('/get_students/<int:subject_id>')
@teacher_required
def get_students(subject_id):
    subject = Subject.query.get(subject_id)
    students = Student.query.filter_by(semester=subject.semester).all()
    return render_template('teacher/_student_list.html', students=students)
