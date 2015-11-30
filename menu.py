from collections import namedtuple
import models
import auth
from app import get_context
from db import make_record, save
import sys  # for sys.exit

Menuoption = namedtuple("Menuoption", "name f")

def _add_customer():
    # TODO: ensure authentication
    db = get_context().db
    customer = models.Customer.new_prompted()
    make_record(db, customer)

def _del_customer():
    # TODO: ensure authentication
    db = get_context().db
    customer_username = input("Username for customer: ")
    customer = db[customer_username]
    print("About to delete the following customer")
    customer.display()
    if input("Are you sure? ").lower().startswith("y"):
        del db[customer]

def _list_customers():
    # TODO: ensure authentication
    db = get_context().db
    print("Username : Name")
    print("---------------")
    for username, record in db.items():
        name = record.user.name
        print("{:8} : {}".format(username, name))

def _edit_customer():
    # TODO: ensure authentication
    db = get_context().db
    customer_username = input("Username for customer: ")
    customer = db[customer_username]
    field_to_edit = input("What field do you want to edit? ")
    try:
        cur_value = getattr(customer, field_to_edit)
    except AttributeError:
        print("Bad customer field {}".format(field_to_edit))
    else:
        print("Current value is {}. What do you want to change it to?".format(cur_value))
        new_value = input(">> ")
        confirm = input("Changing {field} from {old} to {new}. Are you sure? ".format(
            field=field_to_edit,
            old=cur_value,
            new=new_value))
        if confirm.lower().startswith('y'):
            setattr(customer, field_to_edit, new_value)

def _deposit_money():
    context = get_context()
    account = context.user.checking
    print("How much would you like to deposit? Balance: {}".format(account.balance))
    amount = input(":: $ ")
    try:
        account.deposit(amount)
    except Exception:
        print("Deposit failed, your balance has not changed")
        raise
    else:
        print("Thank you! Your new balance is {}".format(account.balance))

def _withdraw_money():
    context = get_context()
    account = context.user.checking
    print("How much would you like to withdraw? Balance: {}".format(account.balance))
    amount = input(":: $ ")
    try:
        account.withdraw(amount)
    except Exception:
        print("Withdrawal failed, your balance has not changed")
        raise
    else:
        print("Thank you! Your new balance is {}".format(account.balance))

def _quit():
    '''Poison pill'''

    context = get_context()
    context.quitting = True

def menu():
    context = get_context()
    if isinstance(context.user, models.Customer):
        options = [Menuoption("Deposit money", _deposit_money),
                   Menuoption("Withdraw money", _withdraw_money),
                   Menuoption("Display info", context.user.display),
                   Menuoption("Log Out", auth.logout)]
    elif isinstance(context.user, models.Admin):
        options = [Menuoption("Add customer", _add_customer),
                   Menuoption("Delete customer", _del_customer),
                   Menuoption("List customers", _list_customers),
                   Menuoption("Edit customer", _edit_customer),
                   Menuoption("Log Out", auth.logout)]
    elif context.user is None:
        options = [Menuoption("Log in", auth.login)]
    options.append(Menuoption("Quit", _quit))  # all states can quit

    opt_dict = {str(idx): option.f for idx,option in enumerate(options, start=1)}

    while True:
        print("MENU")
        for idx, option in enumerate(options, start=1):
            print("{i}. {opt.name}".format(i=idx, opt=option))
        user_in = input(">> ")

        try:
            f = opt_dict[user_in]
        except KeyError:
            print("--- Invalid input {} ---".format(user_in))
            continue
        else:
            f()
            break
