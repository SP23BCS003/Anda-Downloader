from database import get_db, init_db
from models import Settings

def reset_admin_path():
    print("Connecting to database...")
    init_db()
    db = next(get_db())
    
    try:
        setting = db.query(Settings).filter(Settings.key == "admin_panel_url").first()
        if setting:
            print(f"Current path: {setting.value}")
            setting.value = "/admin"
            db.commit()
            print("SUCCESS: Admin path reset to '/admin'")
        else:
            print("Setting 'admin_panel_url' not found. Creating default...")
            s = Settings(key="admin_panel_url", value="/admin", type="string")
            db.add(s)
            db.commit()
            print("SUCCESS: Admin path set to '/admin'")
            
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    confirm = input("Are you sure you want to reset admin path to /admin? (y/n): ")
    if confirm.lower() == 'y':
        reset_admin_path()
