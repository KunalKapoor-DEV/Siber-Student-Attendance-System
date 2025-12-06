from app import create_app
from app.models import User
from werkzeug.security import check_password_hash

app = create_app()

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        print(f"Admin found: {user.username}")
        print(f"Role: {user.role}")
        print(f"Hash: {user.password_hash}")
        if check_password_hash(user.password_hash, 'admin123'):
            print("Password check: SUCCESS")
        else:
            print("Password check: FAILED")
    else:
        print("Admin user NOT found")
