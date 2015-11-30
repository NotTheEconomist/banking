import getpass  # for Customer.new_prompted

class Account(object):
    def __init__(self, owner, type_, balance):
        self.owner = owner
        self.type = type_
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def __str__(self):
        return "Checking account of {o.name}: {b}".format(
            o=self.owner,
            b=self.balance)

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.name = ""

    def serialize(self):
        return ""

class Admin(User):
    pass

class Customer(User):
    def __init__(self, username, password, firstname, lastname, phone, postalcode, checking, savings, dob):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.postalcode = postalcode
        self.checking = Account(self, "checking", checking)
        self.savings = Account(self, "savings", savings)
        self.dob = dob
    
    @property
    def name(self):
        return self.firstname + " " + self.lastname

    @classmethod
    def new_prompted(cls):
        print("Creating new customer...")
        username = input("username: ")
        password = getpass.getpass("password: ")
        firstname, *lastname = input("full name: ")
        dob = input("date of birth: ")
        phone = input("phone: ")
        postalcode = input("postal code: ")
        checking = input("starting balance (checking): ")
        savings = input("starting balance (savings): ")
        return cls(username, password, firstname, lastname, phone, postalcode, checking, savings, dob)


    @classmethod
    def deserialize(cls, line):
        '''initializes Customer from a space-separated line'''

        return cls(*line.split())

    def serialize(self):
        '''serializes to a space-separated line'''

        return "{} {} {} {} {} {} {} {} {}".format(
            self.username,
            self.password,
            self.firstname,
            self.lastname,
            self.phone,
            self.postalcode,
            self.checking.balance,
            self.savings.balance,
            self.dob)

    def display(self):
        print("{name:<50}{phone}{postalcode}{dob}".format(
            name=self.name,
            phone=self.phone,
            postalcode=self.postalcode,
            dob=self.dob))
        print("Checking: {c_balance}".format(c_balance=self.checking.balance))
        print("Savings: {s_balance}".format(s_balance=self.savings.balance))
