from sqlalchemy import create_engine, select, Column
from sqlalchemy.orm import sessionmaker
from userinput import keyboardInput
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from sqlalchemy.types import Integer, String, Date
from models import admin_page
Base = declarative_base()

def getDbConnection(host, username, password, database):
    url = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database}"
    engine = create_engine(url)
    return engine

def create_approval_status(engine):
    Session = sessionmaker(bind=engine)
    session = Session()    
    org_name = keyboardInput("Organization Name: ", str, "Organization Name must be String")
    reg_date = date(
        keyboardInput("Year of Registration: ", int, "Year of Registration must be Integer"),
        keyboardInput("Month of Registration: ", int, "Month of Registration must be Integer"),
        keyboardInput("Day of Registration: ", int, "Day of Registration must be Integer"))
    org_email = keyboardInput("Email Address: ", str, "Email Address must be String")
    org_contact_number = keyboardInput("Contact Number (e.g. 01X-XXXXXXX): ", str, "Contact Number must be String")
    status = keyboardInput("Approval Status: ", str, "Approval Status must be String")
    approval_status = admin_page(org_name=org_name, 
                                 reg_date=reg_date,
                                 org_email=org_email,
                                 org_contact_number = org_contact_number,
                                 status=status)
    session.add(approval_status)
    session.commit()

def list_approval_status(engine):
    Session = sessionmaker(bind=engine)
    session = Session()    
    rows = session.execute(select(admin_page)).scalars().all() 
    try:
        print("=" * 135)
        print(f"{'Id':10s}{'Organization Name':<40s}{'Registration Date':20s}{'Email Address':30s}{'Contact Number':20s}{'Aproval Status'}") 
        print("=" * 135)
        for status in rows:
            print(f"{int(status.id):<10d}{status.org_name:<40s}{status.reg_date.strftime("%Y-%m-%d"):<20s}{status.org_email:30s}{status.org_contact_number:20s}{status.status}") 
        print("=" * 135)
    except Exception as e:
        print("Not able to read the file", e)

def edit_approval_status(engine):
    Session = sessionmaker(bind=engine)
    session = Session()    
    reg_id = keyboardInput("Enter Registration Id: ", int, "Registration Id must be Integer")
    registration = session.get(admin_page, reg_id)
    try:
        id, org_name, year, month, day, org_email, org_contact_number, status = registration.id, registration.org_name, registration.reg_date.year, registration.reg_date.month, registration.reg_date.day, registration.org_email, registration.org_contact_number, registration.status
    except:
        print("Registration Id does not exist")
    else:
        org_name = keyboardInput(f"Organization Name[{org_name}]: ", str, "Organization Name must be String", org_name)
        reg_date = date(
            keyboardInput(f"Year [{year}]: ", int, "Year must be Integer", year),
            keyboardInput(f"Month [{month}]: ", int, "Month must be Integer",month),
            keyboardInput(f"Day [{day}]: ", int, "Day must be Integer",day))
        org_email = keyboardInput("Email Address: ", str, "Email Address must be String", org_email)
        org_contact_number = keyboardInput(f"Contact Number (e.g. 01X-XXXXXXX) [{org_contact_number}]: ", str, "Contact Number must be String", org_contact_number)
        status = keyboardInput(f"Approval Status [{status}]: ", str, "Approval Status must be String", status)
        registration = admin_page(id = reg_id,
                                  org_name = org_name,
                                  reg_date = reg_date,
                                  org_email = org_email,
                                  org_contact_number = org_contact_number,
                                  status = status)
        session.merge(registration)
        session.commit()

def delete_approval_status(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    approval_id = keyboardInput("Enter Approval Id: ", int, "Approval Id must be Integer")
    registration = session.get(admin_page, approval_id)
    try:
        id, org_name, year, month, day, org_email, org_contact_number, status = registration.id, registration.org_name, registration.reg_date.year, registration.reg_date.month, registration.reg_date.day, registration.org_email, registration.org_contact_number, registration.status
    except:
        print("Employe Id does not exist")
    else:
        print(f"Organization Name: {org_name}")
        print(f"Registration Date: {year}{month}{day}")
        print(f"Email Address: {org_email}")
        print(f"Contact Number: {org_contact_number}")
        print(f"Approval Status: {status}")
        confirm = keyboardInput("Are you sure (Y/N): ", str, "Confirm must be string")
        if (confirm == "Y"):
            session.delete(registration)
            session.commit()


def doMenu(engine):
    choice = -1
    while (choice!=0):
        print("===========================")
        print("| 1. List of Registration |")
        print("| 2. Create Registration  |")
        print("| 3. Edit Registration    |")
        print("| 4. Delete Registration  |")
        print("| 0. Exit                 |")
        print("===========================")
        choice = keyboardInput("Enter your choice: ", int, "Choice must be Integer")
        if (choice == 1):
            list_approval_status(engine)
        elif (choice == 2):
            create_approval_status(engine)
        elif (choice == 3):
            edit_approval_status(engine) == 3
        elif (choice == 4):
            delete_approval_status(engine) == 4
        elif (choice == 0):
            print("Thank you")
        else:
            print("Choice can be [0, 1, 2, 3, 4] only") 

engine = getDbConnection("localhost", "root", "root", "loginpage")
doMenu(engine)