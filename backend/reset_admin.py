from database import SessionLocal
from models import Admin
from admin_auth import hash_password

def reset_password():
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == "admin").first()
        if admin:
            print("Found admin user. Resetting password...")
            admin.password_hash = hash_password("admin123")
            db.commit()
            print("Password reset to 'admin123'")
        else:
            print("Admin user not found. Creating one...")
            admin = Admin(
                username="admin",
                password_hash=hash_password("admin123"),
                email="admin@example.com",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created with password 'admin123'")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_password()
