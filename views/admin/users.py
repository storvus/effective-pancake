import bottle

from models.user import User


def users_list(db):
    users = db.query(User).all()
    return bottle.template("admin/users", {"users": users})
