import app
import db
import menu
import sys

database_location = "database.txt"

def init():
    app.make_context()
    db.load(database_location)

if __name__ == "__main__":
    init()
    context = app.get_context()
    while True:
        menu.menu()
        if input("Save changes? ").lower().startswith('y'):
            db.save(database_location)
        if context.quitting:
            sys.exit(0)
