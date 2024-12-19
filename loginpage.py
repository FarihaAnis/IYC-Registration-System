from sqlalchemy import create_engine, select, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from models import login_details
from userinput import keyboardInput
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String


#connect program to the database using SQLAlchemy
def getDbConnection(host, username, password, database):
    url = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database}"
    engine = create_engine(url)
    return engine

def createLogin(engine):
    Session = sessionmaker(bind=engine) #class
    session = Session() #object
    email_address = keyboardInput("Email Address: ", str, "Email Address must be string")
    password = keyboardInput("Password: ", str, "Password must be String")
    account_type = keyboardInput("Account Type: ", str, "Account Type must be a string")
    login = login_details(email=email_address, password=password, account_type=account_type)
    session.add(login)
    session.commit()

def listlogindetails(engine):
    Session = sessionmaker(bind=engine) #class
    session = Session() #object
    rows = session.execute(select(login_details)).scalars().all()
    try:
        print("="*90)
        print(f"{'Id':10s}{'Email Address':40s}{'Password':20s}{'Account Type':20s}")
        print("="*90)
        for login in rows:
            print(f"{int(login.id):<10d}{login.email:40s}{login.password:20s}{login.account_type:20s}")
        print("="*90)
    except Exception as e:
        print("Not able to read the file", e)

def editlogindetails(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    login_id = keyboardInput("Enter login Id: ", int, 
                             "Login Id must be Integer")
    user = session.get(login_details, login_id)
    try:
        id, email, password, account_type = user.id, user.email, user.password, user.account_type
    except:
        print("Login Id does not exist")
    else:
        email_address = keyboardInput(f"Email Address [{email}: ]", str, "Email Address must be string", email)
        password = keyboardInput(f"Password [{password}]: ", str, "Password must be String", password)
        account_type = keyboardInput(f"Account Type [{account_type}]: ", str, "Account Type must be a string", account_type)       
        login = login_details(id = login_id, email=email_address, password=password, account_type=account_type)
        session.merge(login)
        session.commit()

def deletelogindetails(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    login_id = keyboardInput("Enter login Id: ", int, "Login Id must be Integer")
    user = session.get(login_details, login_id)
    try:
        id, email, password, account_type = user.id, user.email, user.password, user.account_type
    except:
        print("Login Id does not exist")
    else:
        print(f"Email Address: {email}")
        print(f"Password: {password}")
        print(f"Account Type: {account_type}")
        confirm = keyboardInput("Are you sure (Y/N): ", str, "Confirm must be string")
        if (confirm == "Y"):
            session.delete(user)
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
            listlogindetails(engine)
        elif (choice == 2):
            createLogin(engine)
        elif (choice == 3):
            editlogindetails(engine) == 3
        elif (choice == 4):
            deletelogindetails(engine) == 4
        elif (choice == 0):
            print("Thank you")
        else:
            print("Choice can be [0, 1, 2, 3, 4] only") 


try:
    engine = getDbConnection("localhost", "root", "root", "loginpage")
except Exception as e:
    print(e)

doMenu(engine)