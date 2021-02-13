from models.user import UserModel
from werkzeug.security import safe_str_cmp
'''users = [
    User(1, 'bob', 'asdf')
]
# created a dictionary that has index on username
username_mapping = { u.username : u for u in users}
# created another dictionary that has index on the user_id
userid_mapping = { u.id: u for u in users }'''
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
