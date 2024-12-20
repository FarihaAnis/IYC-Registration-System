# IYC Registration System
**This project is for learning purposes only.**

## About the Project
The **IYC Registration System** is a web application designed to manage registrations and logins for two types of users: **employees** and **customers**. It uses **Flask** for backend development and **MySQL** to manage and store user data securely. The system follows a simple yet effective structure to ensure smooth user experience and data management.

## Key Features
- **Employee and Customer Accounts**: Separate login systems for employees and customers.
- **Secure Authentication**: Validates user credentials during login.
- **Role-Based Dashboards**:
  - Customers: View and update their account details.
  - Employees: Manage customer accounts, including approvals and deletions.
- **CRUD Functionality**:
  - **Create**: Register new customers and employees.
  - **Read**: Display user and registration details.
  - **Update**: Edit user information (e.g., name, email).
  - **Delete**: Remove user or customer accounts when needed.
- **Database with Relationships**:
  - Proper use of **primary keys** for unique identification.
  - **Foreign keys** to maintain relationships between users, accounts, and records.

## How the System Works

### 1. User Types

#### Customers
- Can register for an account by providing their details.
- Access their dashboard to view or update personal information.

#### Employees
- New employees must register for an account before logging in.
- After registering, employees can log in to access the admin dashboard.
- **Admin Dashboard Responsibilities**:
  - View customer accounts and details.
  - Approve or reject customer account registrations.
  - Delete customer records when necessary.

### 2. Database Overview
The project uses a **MySQL database** with tables designed for storing user information, employee details, and customer records. Key aspects of the database include:
- **Primary Keys**: Ensure each record is uniquely identifiable.
- **Foreign Keys**: Maintain relationships between tables (e.g., linking accounts with customer and employee details).
- **Cascade Deletion**: Automatically removes dependent records when related data is deleted.

### 3. Backend (Flask)
The project implements the **CRUD** concept using Flask:
- **Create**: Adds new customers and employees to the database.
- **Read**: Displays customer and employee details on dashboards.
- **Update**: Allows editing of user information.
- **Delete**: Employees can remove customer accounts when necessary.

### 4. Frontend (HTML and CSS)
- Pages include:
  - **Registration Form**: Captures user details.
  - **Login Page**: Separate login options for customers and employees.
  - **Dashboards**:
    - Customer Dashboard: Shows personal information.
    - Admin Dashboard: Allows employees to manage customer data.
- Bootstrap ensures a clean and responsive design.

## Summary
This project demonstrates how to build a registration system with role-based access and implement CRUD functionality using Flask and MySQL. It also highlights the use of a well-structured database with primary and foreign keys to ensure efficient data management. 
