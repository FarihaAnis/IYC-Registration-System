from sqlalchemy import create_engine, select, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from models import account_reg
from userinput import keyboardInput
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String

def getDbConnection(host, username, password, database):
    url = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database}"
    engine = create_engine(url)
    return engine

def create_acc(engine):
    Session = sessionmaker(bind=engine) #class
    session = Session() #object
    email_address = keyboardInput("Email Address: ", str, "Email Address must be string")
    password = keyboardInput("Password: ", str, "Password must be String")
    create = account_reg(email=email_address, password=password)
    session.add(create)
    session.commit()

def list_acc(engine):
    Session = sessionmaker(bind=engine) #class
    session = Session() #object
    rows = session.execute(select(account_reg)).scalars().all()
    try:
        print("="*90)
        print(f"{'Id':10s}{'Email Address':40s}{'password':20s}")
        print("="*90)
        for acc in rows:
            print(f"{int(acc.id):<10d}{acc.email:40s}{acc.password:20s}")
        print("="*90)
    except Exception as e:
        print("Not able to read the file", e)

def edit_acc(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    acc_id = keyboardInput("Enter Account Id: ", int, 
                             "Account Id must be Integer")
    account = session.get(account_reg, acc_id)
    try:
        id, email, new_password = account.id, account.email, account.password
    except:
        print("Login Id does not exist")
    else:
        email_address = keyboardInput(f"Email Address [{email}: ]", str, "Email Address must be string", email)
        password = keyboardInput(f"New_password [{new_password}]: ", str, "Password must be String", password)
        edit = account_reg(id = acc_id, email=email_address, password=password)
        session.merge(edit)
        session.commit()

def delete_acc(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    acc_id = keyboardInput("Enter Account Id: ", int, "Account Id must be Integer")
    account = session.get(account_reg, acc_id)
    try:
        id, email, password = account.id, account.email, account.password
    except:
        print("Account Id does not exist")
    else:
        print(f"Email Address: {email}")
        print(f"New_password: {password}")
        confirm = keyboardInput("Are you sure (Y/N): ", str, "Confirm must be string")
        if (confirm == "Y"):
            session.delete(account)
            session.commit()

def doMenu(engine):
    choice = -1
    while (choice!=0):
        print("============================")
        print("| 1. List Login Details    |")
        print("| 2. Create Login Details  |")
        print("| 3. Edit Login Details    |")
        print("| 4. Delete Login Details  |")
        print("| 0. Exit                  |")
        print("============================")
        choice = keyboardInput("Enter your choice: ", int, "Choice must be Integer")
        if (choice == 1):
            list_acc(engine)
        elif (choice == 2):
            create_acc(engine)
        elif (choice == 3):
            edit_acc(engine) == 3
        elif (choice == 4):
            delete_acc(engine) == 4
        elif (choice == 0):
            print("Thank you")
        else:
            print("Choice can be [0, 1, 2, 3, 4] only") 


try:
    engine = getDbConnection("localhost", "root", "root", "loginpage")
except Exception as e:
    print(e)

doMenu(engine)
