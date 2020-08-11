from werkzeug.security import safe_str_cmp
from user import User


users = [User(1, 'florin', 'asdf')]

username_mapping ={user.username:  user for user in users}


userid_mapping = {user._id : user for user in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)  #get method give the value of the key
    if user and safe_str_cmp(user.password, password): #function to compare 2 strings
        return user

def identity(payload):
   user_id = payload['identity']
   userid_mapping.get(user_id, None)