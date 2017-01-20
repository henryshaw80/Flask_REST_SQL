from src.user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'bob', '123')
]
username_mapping = {u.username: u for u in users} #set comprehension
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    # if there isn't username key, default value is None
    user = username_mapping.get(username, None)

    # safe_str_cmp is comparing two strings
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
