from database import get_db, init_db
from models import Settings

def check_admin_url():
    print("Connecting to database...")
    init_db()
    db = next(get_db())
    
    try:
        setting = db.query(Settings).filter(Settings.key == "admin_panel_url").first()
        if setting:
            print(f"Current DATABASE value for 'admin_panel_url': '{setting.value}'")
        else:
            print("Setting 'admin_panel_url' NOT FOUND in database.")
            
        # Also check other relevant settings
        site_name = db.query(Settings).filter(Settings.key == "site_name").first()
        print(f"Site Name: {site_name.value if site_name else 'Not Set'}")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_url()
