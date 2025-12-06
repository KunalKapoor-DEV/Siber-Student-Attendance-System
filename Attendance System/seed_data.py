from app import create_app, db
from app.models import User, Teacher, Student, Subject
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Seeding data...")

    # Create Demo Teacher
    if not User.query.filter_by(username='teacher').first():
        user = User(username='teacher', password_hash=generate_password_hash('teacher123', method='pbkdf2:sha256'), role='teacher')
        db.session.add(user)
        db.session.commit()
        
        teacher = Teacher(user_id=user.id, name='Demo Teacher', email='teacher@siber.edu.in')
        db.session.add(teacher)
        print("Created Teacher: teacher@siber.edu.in / teacher123")
    else:
        print("Teacher already exists.")

    # Create Demo Student
    if not User.query.filter_by(username='student').first():
        user = User(username='student', password_hash=generate_password_hash('student123', method='pbkdf2:sha256'), role='student')
        db.session.add(user)
        db.session.commit()
        
        student = Student(user_id=user.id, name='Demo Student', prn='2023001', semester=1)
        db.session.add(student)
        print("Created Student: PRN 2023001 / student123")
    else:
        print("Student already exists.")

    # Create Demo Subject
    if not Subject.query.filter_by(name='Python Programming').first():
        subject = Subject(name='Python Programming', semester=1)
        db.session.add(subject)
        print("Created Subject: Python Programming")
    else:
        print("Subject already exists.")

    db.session.commit()
    print("Seeding complete.")

    db.session.commit()
    print("Seeding complete.")
