from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db, User, Teacher, Student, Subject
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You must be an admin to access this page.')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='admin').first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid admin credentials')
            
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    teacher_count = Teacher.query.count()
    student_count = Student.query.count()
    subject_count = Subject.query.count()
    return render_template('admin/dashboard.html', 
                           teacher_count=teacher_count, 
                           student_count=student_count, 
                           subject_count=subject_count)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('admin.add_user'))
            
        user = User(username=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'), role=role)
        db.session.add(user)
        db.session.commit()
        
        if role == 'teacher':
            email = request.form.get('email')
            teacher = Teacher(user_id=user.id, name=name, email=email)
            db.session.add(teacher)
        elif role == 'student':
            prn = request.form.get('prn')
            semester = request.form.get('semester')
            student = Student(user_id=user.id, name=name, prn=prn, semester=semester)
            db.session.add(student)
            
        db.session.commit()
        flash(f'{role.capitalize()} added successfully')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/add_user.html')

@admin_bp.route('/subjects/add', methods=['GET', 'POST'])
@admin_required
def add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        semester = request.form.get('semester')
        
        subject = Subject(name=name, semester=semester)
        db.session.add(subject)
        db.session.commit()
        
        flash('Subject added successfully')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/add_subject.html')
