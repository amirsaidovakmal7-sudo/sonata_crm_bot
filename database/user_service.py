from database import get_db
from database.models import User



def create_user(tg_id, language):
    db = next(get_db())
    user = db.query(User).filter(User.tg_id==tg_id).first()
    if not user:
        new_user = User(tg_id=tg_id, choosed_language=language)
        db.add(new_user)
        db.commit()
        return True
    else:
        return False


def get_user(tg_id):
    db = next(get_db())
    user = db.query(User).filter(User.tg_id==tg_id).first()
    if user:
        return user
    return False


def get_user_language_bd(tg_id):
    db = next(get_db())
    user = db.query(User).filter(User.tg_id==tg_id).first()
    if user:
        return user.choosed_language
    return False


