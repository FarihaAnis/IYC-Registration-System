from flask import Flask, render_template, request, redirect, url_for, session
from models import Base, login_details, account_reg, employee_reg_acc, admin_page, CustomerAccount
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from validate_password import validate_password
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'iyc_registration_page'

def getDbConnection(host, username, password, database):
    url = f"mysql+mysqlconnector://{username}:{password}@{host}:3306/{database}"
    engine = create_engine(url)
    return engine
engine = getDbConnection("localhost", "root", "root", "hostel_management_system")

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    Session = sessionmaker(bind=engine)
    session_db = Session()
    email_address = request.form.get('email')
    password = request.form.get('password')
    
    if not email_address or not password:
        return render_template('login.html', error="Please provide both email and password.")
    
    try:
        # Check if login is for a customer FIRST
        account_customer = session_db.query(CustomerAccount).filter_by(email_address=email_address).first()
        if account_customer and account_customer.account.password == password:
            # Update login_details table
            login_detail = login_details(
                email=email_address,
                password=password,
                account_type='customer'
            )
            session_db.add(login_detail)
            session_db.commit()
            
            # Set session variables
            session['email'] = email_address
            session['account_type'] = 'customer'
            session['customer_id'] = account_customer.id  # Store customer ID for profile access
            return redirect(url_for('view', id=account_customer.id))  # Redirect to customer profile page
        
        # If no match is found for customers, check for employees
        account_employee = session_db.query(account_reg).filter_by(email=email_address).first()
        if account_employee and account_employee.password == password:
            # Update login_details table
            login_detail = login_details(
                email=email_address,
                password=password,
                account_type='employee'
            )
            session_db.add(login_detail)
            session_db.commit()
            
            # Set session variables
            session['email'] = email_address
            session['account_type'] = 'employee'
            return redirect(url_for('admin'))  # Redirect to admin page
        
        # If no account matches
        return render_template('login.html', error="Invalid email or password.")
    
    except Exception as e:
        session_db.rollback()
        print(f"Error during login: {e}")
        return render_template('login.html', error="An unexpected error occurred. Please try again.")
    finally:
        session_db.close()
  
@app.route('/account_registration', methods=['GET', 'POST'])
def account_registration():
    # Retrieve user_type from request.args for GET, and from request.form for POST
    user_type = request.args.get('user_type') if request.method == 'GET' else request.form.get('user_type')

    if request.method == 'POST':
        Session = sessionmaker(bind=engine)
        session = Session()

        # Get form data
        email_address = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate password based on the custom rules
        is_valid, message = validate_password(password)
        if not is_valid:
            return render_template('account_reg.html', error=message, user_type=user_type)

        if password != confirm_password:
            return render_template('account_reg.html', error="Passwords do not match.", user_type=user_type)

        try:
            new_account = account_reg(email=email_address, password=password)
            session.add(new_account)
            session.commit()

            # Redirect based on user type
            if user_type == 'customer':
                return redirect(url_for('customer_registration'))
            else:
                return redirect(url_for('employee_registration'))
        except Exception as e:
            session.rollback()
            return render_template('account_reg.html', error=str(e), user_type=user_type)
        finally:
            session.close()

    return render_template('account_reg.html', user_type=user_type)


@app.route('/employee_registration', methods=['GET', 'POST'])
def employee_registration():
    if request.method == 'POST':
        Session = sessionmaker(bind=engine)
        db_session = Session()  # Renamed local variable

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        job_title = request.form.get('job_title')
        department = request.form.get('department')
        gender = request.form.get('gender')
        date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date()
        marital_status = request.form.get('marital_status')
        email = request.form.get('email')
        contact_number = request.form.get('contact_number')
        street_address = request.form.get('street_address')
        city = request.form.get('city')
        state = request.form.get('state')
        postcode = request.form.get('postcode')
        country = request.form.get('country')

        try:
            latest_account = db_session.query(account_reg).filter_by(email=email).first()
            if latest_account is None:
                raise Exception("No account registration found for this email. Please create an account first.")
            
            new_employee = employee_reg_acc(
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
                city=city,
                state=state,
                postcode=postcode,
                country=country,
                employee_id=latest_account.id
            )
            db_session.add(new_employee)
            db_session.commit()

            # Set session variables
            session['email'] = email
            session['account_type'] = 'employee'

            return redirect(url_for('admin'))
        
        except Exception as e:
            db_session.rollback()
            return render_template('employee_reg.html', error=str(e))
        finally:
            db_session.close()

    return render_template('employee_reg.html')


@app.route('/admin')
def admin():
    if session.get('account_type') != 'employee':
        return redirect(url_for('index'))  # Redirect non-employees to the login page
    
    Session = sessionmaker(bind=engine)
    session_db = Session()
    try:
        organizations = session_db.query(admin_page).all()
        return render_template('admin.html', organizations=organizations)
    finally:
        session_db.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Customer route
@app.route('/customer_registration', methods=['GET', 'POST'])
def customer_registration():
    if request.method == 'POST':
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            # Retrieve form data
            organization_name = request.form.get('organization_name')
            ssm_number = request.form.get('ssm_number')
            email_address = request.form.get('email_address')
            contact_number = request.form.get('contact_number')
            street_address = request.form.get('street_address')
            city = request.form.get('city')
            state = request.form.get('state')
            postcode = request.form.get('postcode')
            country = request.form.get('country')
            purpose = request.form.get('purpose')
            submission_date = datetime.now()

            # Fetch the account_id from account_reg table using email_address
            account = session.query(account_reg).filter_by(email=email_address).first()
            if not account:
                raise Exception("No registered account found for the provided email. Please register first.")
            
            # Step 1: Create a new customer record
            new_customer = CustomerAccount(
                organization_name=organization_name,
                submission_date=submission_date,
                ssm_number=ssm_number,
                email_address=email_address,
                contact_number=contact_number,
                street_address=street_address,
                city=city,
                state=state,
                postcode=postcode,
                country=country,
                purpose=purpose,
                account_id=account.id,
                approval_status=0
            )
            session.add(new_customer)
            session.flush()

            # Step 2: Automatically add the organization details to admin_page
            new_admin_entry = admin_page(
                org_name=organization_name,
                reg_date=submission_date.date(),
                org_email=email_address,
                org_contact_number=contact_number,
                status="Pending",  # Default status for new registrations
                customer_account_id=new_customer.id  # Link to the CustomerAccount
            )
            session.add(new_admin_entry)

            # Commit all changes to the database
            session.commit()

            # Redirect to the success page after registration
            return render_template('successful_reg.html')

        except Exception as e:
            session.rollback()
            print(f"Database Error: {str(e)}")
            return render_template('customer_registration.html', error="An error occurred while saving the data. Please try again.")
        finally:
            session.close()

    return render_template('customer_registration.html')

    
@app.route('/customer_edit/<int:id>', methods=['GET', 'POST'])
def customer_edit(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    # Query the database for the customer account using the provided ID
    account = session.query(CustomerAccount).filter_by(id=id).first()

    if not account:
        return "Account not found", 404

    if request.method == 'POST':
        # Update the account with the new data from the form
        account.organization_name = request.form['organization_name']
        account.ssm_number = request.form['ssm_number']
        account.email_address = request.form['email_address']
        account.contact_number = request.form['contact_number']
        account.street_address = request.form['street_address']
        account.city = request.form['city']
        account.state = request.form['state']
        account.postcode = request.form['postcode']
        account.country = request.form['country']
        account.purpose = request.form['purpose']
        
        # Commit the changes to the database
        session.commit()

        return redirect(url_for('customer_view', account_id=id))

    # Render the edit form with the existing account data
    return render_template('customer_edit.html', account=account)


@app.route('/view', methods=['GET'])
def view():
    Session = sessionmaker(bind=engine)
    session_db = Session()
    account_id = request.args.get('id')  # Retrieve account ID from the query string

    try:
        # Fetch the customer account by ID
        account = session_db.query(CustomerAccount).filter_by(id=account_id).first()

        if not account:
            return "Account not found", 404

        # Check if the user is an employee or a customer
        if session.get('account_type') == 'employee':
            # Allow employees to view the customer profile
            return render_template('customer_profile.html', accounts=[account])
        elif session.get('account_type') == 'customer' and session.get('customer_id') == int(account_id):
            # Allow customers to view their own profile
            return render_template('customer_profile.html', accounts=[account])
        else:
            # Restrict access for others
            return redirect(url_for('index'))
    finally:
        session_db.close()

@app.route('/delete', methods=['POST'])
def delete_registration():
    Session = sessionmaker(bind=engine)
    session = Session()
    approval_id = request.form.get('id')  # Correctly retrieve the ID from the form
    try:
        # Query the admin_page table to find the record by ID
        registration = session.query(admin_page).filter_by(id=approval_id).first()
        if registration:
            session.delete(registration)
            session.commit()

        # After deletion, re-query the database to get the updated list of organizations
        organizations = session.query(admin_page).all()
        return render_template('admin.html', organizations=organizations)
    except Exception as e:
        session.rollback()
        return str(e)
    finally:
        session.close()

@app.route('/approve_customer/<int:id>', methods=['POST'])
def approve_customer(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Update CustomerAccount table
        account = session.query(CustomerAccount).filter_by(id=id).first()
        if account:
            account.approval_status = True  # Mark as Approved

            # Update admin_page table linked to this customer account
            admin_entry = session.query(admin_page).filter_by(customer_account_id=id).first()
            if admin_entry:
                admin_entry.status = "Approved"  # Set status to Approved
            
            session.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        session.rollback()
        return str(e)
    finally:
        session.close()

@app.route('/reject_customer/<int:id>', methods=['POST'])
def reject_customer(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Update CustomerAccount table
        account = session.query(CustomerAccount).filter_by(id=id).first()
        if account:
            account.approval_status = False  # Mark as Rejected

            # Update admin_page table linked to this customer account
            admin_entry = session.query(admin_page).filter_by(customer_account_id=id).first()
            if admin_entry:
                admin_entry.status = "Rejected"  # Set status to Rejected
            
            session.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        session.rollback()
        return str(e)
    finally:
        session.close()

