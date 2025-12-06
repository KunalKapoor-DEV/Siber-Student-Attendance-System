from flask import Flask, redirect, url_for
from .database import db
from .models import User
from flask_login import LoginManager
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-prod'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'  <-- Removed to allow custom handling
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints (Placeholders for now)
    # Auth Blueprint removed - Auth is now distributed across portals
    
    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .routes.teacher import teacher_bp
    app.register_blueprint(teacher_bp)
    
    from .routes.student import student_bp
    app.register_blueprint(student_bp)

    @app.route('/')
    def index():
        # For now, just show a simple landing page or redirect to one of the portals
        return "<h1>Welcome to CSIBER Attendance System</h1><p><a href='/admin/login'>Admin</a> | <a href='/teacher/login'>Teacher</a> | <a href='/student/login'>Student</a></p>"

    with app.app_context():
        db.create_all()
        # Create a default admin if not exists
        if not User.query.filter_by(role='admin').first():
            from werkzeug.security import generate_password_hash
            admin = User(username='admin', password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'), role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin / admin123")

    return app
