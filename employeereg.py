from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from userinput import keyboardInput
from datetime import date
from sqlalchemy.types import Integer, String, Date
from models import employee_reg_acc

def getDbConnection(host, username, password, database):
    url = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database}"
    engine = create_engine(url)
    return engine

def create_employee_acc(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    first_name = keyboardInput("First Name: ", str, "First Name must be String")
    last_name = keyboardInput("Last Name: ", str, "Last Name must be String")
    job_title = keyboardInput("Job Title: ", str, "Job Title must be String")
    department = keyboardInput("Department: ", str, "Department must be String")
    gender = keyboardInput("Gender: ", str, "Gender must be String")
    date_of_birth = date(
        keyboardInput("Year of Birth: ", int, "Year of Birth must be Integer"),
        keyboardInput("Month of Birth: ", int, "Month of Birth must be Integer"),
        keyboardInput("Day of Birth: ", int, "Day must be Integer"))
    marital_status = keyboardInput("Marital Status (Single/Married): ", str, "Marital Status must be String")
    email = keyboardInput("Email Address: ", str, "Email Address must be String")
    contact_number = keyboardInput("Contact Number (e.g. 012-XXXXXXX): ", str, "Contact Number must be String")
    street_address = keyboardInput("Street Address: ", str, "Street Address must be String")
    city = keyboardInput("City: ", str, "City must be String")
    state = keyboardInput("State: ", str, "State must be String")
    postcode = keyboardInput("Postcode: ", str, "Postcode must be String")
    country = keyboardInput("Country: ", str, "Country must be String")
    employee_id = keyboardInput("Employee Id: ", int, "Employee Id must be Integer")
    employee_acc = employee_reg_acc(first_name=first_name, 
                                    last_name=last_name, 
                                    job_title=job_title, 
                                    department=department, 
                                    gender=gender, 
                                    date_of_birth=date_of_birth,
                                    marital_status=marital_status, 
                                    email=email, 
                                    contact_number=contact_number,
                                    street_address=street_address, 
                                    city=city, state=state, 
                                    postcode=postcode,
                                    country=country,
                                    employee_id=employee_id)
    session.add(employee_acc)
    session.commit()
    print("Employee account created successfully!")

def list_employee(engine):
    Session = sessionmaker(bind=engine) #class
    session = Session() #object
    rows = session.execute(select(employee_reg_acc)).scalars().all()
    try:
        print("="*265)
        print(f"{'Id':5s}{'First Name':15s}{'Last Name':15s}{'Job Title':15s}{'Department':15s}{'Gender':10s}{'Date of Birth':20s}{'Marital Status':20s}{'Email Address':30s}{'Contact Number':20s}{'Street Address':45s}{'City':15s}{'State':15s}{'Postcode':15s}{'Country'}") 
        print("="*265)
        for employee in rows:
            print(f"{int(employee.id):<5d}{employee.first_name:15s}{employee.last_name:15s}{employee.job_title:15s}{employee.department:15s}{employee.gender:10s}{employee.date_of_birth.strftime("%Y-%m-%d"):<20s}{employee.marital_status:20s}{employee.email:30s}{employee.contact_number:20s}{employee.street_address:45s}{employee.city:15s}{employee.state:15s}{int(employee.postcode):<15d}{employee.country}")
        print("="*265)
    except Exception as e:
        print("Not able to read the file", e)

def edit_employee_acc(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    employee_id = keyboardInput("Enter Employee Id: ", int, "Employee Id must be Integer")
    employee = session.get(employee_reg_acc, employee_id)
    try:
        id, first_name, last_name, job_title, department, gender, year, month, day, marital_status, email, contact_number, street_address, city, state, postcode, country = employee.id, employee.first_name, employee.last_name, employee.job_title, employee.department, employee.gender, employee.date_of_birth.year, employee.date_of_birth.month, employee.date_of_birth.day, employee.marital_status, employee.email, employee.contact_number, employee.street_address, employee.city, employee.state, employee.postcode, employee.country
    except:
        print("Employee Id does not exist")
    else:
        first_name = keyboardInput(f"First Name [{first_name}]: ", str, "First Name must be String", first_name)
        last_name = keyboardInput(f"Last Name [{last_name}]: ", str, "Last Name must be String", last_name)
        job_title = keyboardInput(f"Job Title [{job_title}]: ", str, "Job Title must be String", job_title)
        department = keyboardInput(f"Department [{department}]: ", str, "Department must be String", department)
        gender = keyboardInput(f"Gender [{gender}]: ", str, "Gender must be String", gender)
        date_of_birth = date(
            keyboardInput(f"Year of Birth [{year}]: ", int, "Year of Birth must be Integer", year),
            keyboardInput(f"Month of Birth [{month}]: ", int, "Month of Birth must be Integer",month),
            keyboardInput(f"Day of Birth [{day}]: ", int, "Day must be Integer",day))
        marital_status = keyboardInput("Marital Status (Single/Married): ", str, "Marital Status must be String", marital_status)
        email = keyboardInput("Email Address: ", str, "Email Address must be String", email)
        contact_number = keyboardInput(f"Contact Number (e.g. 01X-XXXXXXX) [{contact_number}]: ", str, "Contact Number must be String", contact_number)
        street_address = keyboardInput("Street Address: ", str, "Street Address must be String", street_address)
        city = keyboardInput("City: ", str, "City must be String", city)
        state = keyboardInput("State: ", str, "State must be String", state)
        postcode = keyboardInput("Postcode: ", int, "Postcode must be String", postcode)
        country = keyboardInput("Country: ", str, "Country must be String", country)
        employee_acc = employee_reg_acc(id = employee_id, 
                                        first_name=first_name, 
                                        last_name=last_name, 
                                        job_title=job_title, 
                                        department=department, 
                                        gender=gender, 
                                        date_of_birth=date_of_birth,
                                        marital_status=marital_status, 
                                        email=email, 
                                        contact_number=contact_number,
                                        street_address=street_address, 
                                        city=city, state=state, 
                                        postcode=postcode,
                                        country=country)
        session.merge(employee_acc)
        session.commit()

def delete_employee_acc(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    employee_id = keyboardInput("Enter Employee Id: ", int, "Employee Id must be Integer")
    employee = session.get(employee_reg_acc, employee_id)
    try:
        id, first_name, last_name, job_title, department, gender, year, month, day, marital_status, email, contact_number, street_address, city, state, postcode, country = employee.id, employee.first_name, employee.last_name, employee.job_title, employee.department, employee.gender, employee.date_of_birth.year, employee.date_of_birth.month, employee.date_of_birth.day, employee.marital_status, employee.email, employee.contact_number, employee.street_address, employee.city, employee.state, employee.postcode, employee.country
    except:
        print("Employe Id does not exist")
    else:
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Job Title: {job_title}")
        print(f"Department: {department}")
        print(f"Gender: {gender}")
        print(f"Date of Birth: {year}{month}{day}")
        print(f"Marital Status: {marital_status}")
        print(f"Email: {email}")
        print(f"Contact Number: {contact_number}")
        print(f"Street Address: {street_address}")
        print(f"City: {city}")
        print(f"State: {state}")
        print(f"Postcode: {postcode}")
        print(f"Country: {country}")
        confirm = keyboardInput("Are you sure (Y/N): ", str, "Confirm must be string")
        if (confirm == "Y"):
            session.delete(employee)
            session.commit()
    

try:
    engine = getDbConnection("localhost", "root", "root", "loginpage")
except Exception as e:
    print(e)

def doMenu(engine):
    choice = -1
    while (choice!=0):
        print("===============================")
        print("| 1. List of Employees Account|")
        print("| 2. Create Employee Account  |")
        print("| 3. Edit Employee Account    |")
        print("| 4. Delete Employee Account  |")
        print("| 0. Exit                     |")
        print("===============================")
        choice = keyboardInput("Enter your choice: ", int, "Choice must be Integer")
        if (choice == 1):
            list_employee(engine)
        elif (choice == 2):
            create_employee_acc(engine)
        elif (choice == 3):
            edit_employee_acc(engine) == 3
        elif (choice == 4):
            delete_employee_acc(engine) == 4
        elif (choice == 0):
            print("Thank you")
        else:
            print("Choice can be [0, 1, 2, 3, 4] only") 

doMenu(engine)