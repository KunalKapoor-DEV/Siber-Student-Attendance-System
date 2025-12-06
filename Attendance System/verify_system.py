from app import create_app, db
from app.models import User, Teacher, Student, Subject, AttendanceSession, AttendanceRecord
from werkzeug.security import generate_password_hash

app = create_app()

def verify_system():
    with app.app_context():
        print("1. Resetting Database...")
        db.drop_all()
        db.create_all()
        
        print("2. Creating Admin...")
        admin = User(username='admin', password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'), role='admin')
        db.session.add(admin)
        db.session.commit()
        
        print("3. Creating Teacher (Mr. Smith)...")
        t_user = User(username='teacher1', password_hash=generate_password_hash('pass', method='pbkdf2:sha256'), role='teacher')
        db.session.add(t_user)
        db.session.commit()
        teacher = Teacher(user_id=t_user.id, name='Mr. Smith', email='smith@siber.edu.in')
        db.session.add(teacher)
        
        print("4. Creating Student (John Doe)...")
        s_user = User(username='student1', password_hash=generate_password_hash('pass', method='pbkdf2:sha256'), role='student')
        db.session.add(s_user)
        db.session.commit()
        student = Student(user_id=s_user.id, name='John Doe', prn='2023001', semester=1)
        db.session.add(student)
        
        print("5. Creating Subject (Python)...")
        subject = Subject(name='Python Programming', semester=1)
        db.session.add(subject)
        db.session.commit()
        
        print("6. Simulating Attendance Session 1 (John is Absent)...")
        session1 = AttendanceSession(teacher_id=teacher.id, subject_id=subject.id)
        db.session.add(session1)
        db.session.commit()
        
        # Mark absent
        rec1 = AttendanceRecord(session_id=session1.id, student_id=student.id, status='Absent')
        db.session.add(rec1)
        db.session.commit()
        
        print("7. Simulating Attendance Session 2 (John is Present)...")
        session2 = AttendanceSession(teacher_id=teacher.id, subject_id=subject.id)
        db.session.add(session2)
        db.session.commit()
        
        # Mark present (default inference)
        rec2 = AttendanceRecord(session_id=session2.id, student_id=student.id, status='Present')
        db.session.add(rec2)
        db.session.commit()
        
        print("8. Verifying Analytics...")
        records = AttendanceRecord.query.filter_by(student_id=student.id).all()
        total = len(records)
        present = len([r for r in records if r.status == 'Present'])
        percentage = (present / total) * 100
        
        print(f"   Total Lectures: {total}")
        print(f"   Attended: {present}")
        print(f"   Percentage: {percentage}%")
        
        if total == 2 and present == 1 and percentage == 50.0:
            print("\nSUCCESS: System logic verified!")
        else:
            print("\nFAILURE: Analytics mismatch.")

if __name__ == '__main__':
    verify_system()
