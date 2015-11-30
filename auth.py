ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"
from app import get_context
import getpass

class AlreadyLoggedInError(RuntimeError):
    pass

def authenticate_user(db, given_username, given_password):
    try:
        if db[given_username].password == given_password:
            return db[given_username].user
    except IndexError:
        return False

def login():
    '''Prompt for login'''
    context = get_context()
    print("LOGIN")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    if context.user:
        print("User {} is already logged in")
        return
    user = authenticate_user(context.db, username, password)
    if user:
        context.user = user
    else:
        print("Invalid username or password")

def logout():
    context = get_context()
    context.user = None
