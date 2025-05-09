from sqlalchemy.orm import Session
from models import Setting

def is_booking_enabled(db: Session) -> bool:
    setting = db.query(Setting).filter(Setting.key == "booking_enabled").first()
    return setting and setting.value.lower() == "true"

def set_booking_enabled(db: Session, enabled: bool):
    setting = db.query(Setting).filter(Setting.key == "booking_enabled").first()
    if setting:
        setting.value = "true" if enabled else "false"
    else:
        setting = Setting(key="booking_enabled", value="true" if enabled else "false")
        db.add(setting)
    db.commit()
    return setting.value
