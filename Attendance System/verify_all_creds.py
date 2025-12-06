from app import create_app
from app.models import User
from werkzeug.security import check_password_hash

app = create_app()

def check_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"User found: {user.username} (Role: {user.role})")
        if check_password_hash(user.password_hash, password):
            print(f"  > Password '{password}': VALID")
        else:
            print(f"  > Password '{password}': INVALID")
    else:
        print(f"User '{username}' NOT found")

with app.app_context():
    print("--- Verifying Credentials ---")
    check_user('admin', 'admin123')
    check_user('teacher1', 'teacher1')
    check_user('student1', 'student1')
