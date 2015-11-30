from collections import namedtuple
from models import Customer, Admin
from auth import ADMIN_USERNAME, ADMIN_PASSWORD 
from app import get_context

Record = namedtuple("Record", "password user")

def make_record(db, customer):
    db[customer.username] = Record(customer.password, customer)

def load(filename):
    context = get_context()
    db = {}
    admin = Admin(ADMIN_USERNAME, ADMIN_PASSWORD)
    make_record(db, admin)
    try:
        with open(filename) as db_f:
            customers = [Customer.deserialize(line) for line in db_f if line.strip()]
            for customer in customers:
                make_record(db, customer)
    except FileNotFoundError:
        print("No such database. Save first?")
    context.db = db

def save(filename):
    db = get_context().db
    with open(filename, 'w') as db_f:
        for record in db.values():
            customer = record.user
            db_f.write("{}\n".format(customer.serialize()))
    print("Updates saved!")
