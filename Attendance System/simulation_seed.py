import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Teacher, Student, Subject, AttendanceSession, AttendanceRecord
from werkzeug.security import generate_password_hash

app = create_app()

def run_simulation():
    with app.app_context():
        print("1. Resetting Database...")
        db.drop_all()
        db.create_all()

        # 2. Create Admin
        print("2. Creating Admin...")
        admin = User(username='admin', password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'), role='admin')
        db.session.add(admin)
        db.session.commit()

        # 3. Create Subjects & Teachers
        print("3. Creating Subjects and Teachers...")
        subjects_list = [
            "C Programming", "Fundamental", "IKS", "Office Automation", 
            "Web Development", "Democracy", "Business Communication", 
            "Sports", "Japanese"
        ]
        
        teachers = []
        subjects = []

        for i, sub_name in enumerate(subjects_list):
            # Create Teacher User
            username = f"teacher{i+1}"
            password = f"teacher{i+1}"
            user = User(username=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'), role='teacher')
            db.session.add(user)
            db.session.commit()
            
            # Create Teacher Profile
            teacher = Teacher(user_id=user.id, name=f"Prof. {sub_name.split()[0]}", email=f"{username}@siber.edu.in")
            db.session.add(teacher)
            teachers.append(teacher)
            
            # Create Subject
            subject = Subject(name=sub_name, semester=2)
            db.session.add(subject)
            subjects.append(subject)
            
            print(f"   Created {sub_name} / {username}")

        db.session.commit()

        # 4. Create Students
        print("4. Creating 75 Students...")
        students = []
        for i in range(1, 76):
            username = f"student{i}"
            password = f"student{i}"
            user = User(username=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'), role='student')
            db.session.add(user)
            db.session.commit()
            
            student = Student(user_id=user.id, name=f"Student {i}", prn=f"2023{i:03d}", semester=2)
            db.session.add(student)
            
            # Assign attendance bias: 
            # - 10% have 100% attendance (bias = 1.0)
            # - 10% are bunkers (bias = 0.4 - 0.6)
            # - Rest are average (bias = 0.7 - 0.95)
            rand_val = random.random()
            if rand_val < 0.1:
                bias = 1.0
            elif rand_val < 0.2:
                bias = random.uniform(0.4, 0.6)
            else:
                bias = random.uniform(0.7, 0.95)
            
            students.append({'obj': student, 'bias': bias})
            
        db.session.commit()
        print("   Students created.")

        # 5. Simulate 90 Days
        print("5. Simulating 90 Days of Attendance...")
        start_date = datetime.now() - timedelta(days=90)
        
        total_sessions = 0
        
        for day in range(90):
            current_date = start_date + timedelta(days=day)
            
            # Skip Sundays (weekday 6)
            if current_date.weekday() == 6:
                continue
                
            # 4 Sessions per day
            daily_subjects = random.sample(range(len(subjects)), 4)
            
            for sub_idx in daily_subjects:
                teacher = teachers[sub_idx]
                subject = subjects[sub_idx]
                
                session = AttendanceSession(teacher_id=teacher.id, subject_id=subject.id, date=current_date)
                db.session.add(session)
                db.session.commit()
                total_sessions += 1
                
                # Mark attendance for all students
                for s_data in students:
                    student = s_data['obj']
                    bias = s_data['bias']
                    
                    # Determine status based on bias
                    status = 'Present' if random.random() < bias else 'Absent'
                    
                    record = AttendanceRecord(session_id=session.id, student_id=student.id, status=status)
                    db.session.add(record)
                
                db.session.commit()
        
        print(f"   Simulation complete. Total Sessions: {total_sessions}")
        print("\nCredentials Summary:")
        print("   Admin: admin / admin123")
        print("   Teachers: teacher1..teacher9 / teacher1..teacher9")
        print("   Students: student1..student75 / student1..student75")

if __name__ == '__main__':
    run_simulation()
