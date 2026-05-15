import bcrypt
from db import add_user, get_user


def register_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    add_user(username, hashed)


def login_user(username, password):
    user = get_user(username)

    if user:
        stored_password = user[2]

        if bcrypt.checkpw(password.encode(), stored_password):
            return True

    return False