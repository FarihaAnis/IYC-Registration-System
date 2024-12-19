from sqlalchemy import create_engine, select, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from userinput import keyboardInput
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from sqlalchemy.types import Integer, String, Date
from sqlalchemy import Integer, String, Column, Enum, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class login_details(Base):
    __tablename__ = "login_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), nullable=False)
    password = Column(String(60), nullable=False)
    account_type = Column(String(60), nullable=False)


class admin_page(Base):
    __tablename__ = "admin_page"
    id = Column(Integer, primary_key=True, autoincrement=True)
    org_name = Column(String(120), nullable=False)
    reg_date = Column(Date, nullable=False)
    org_email = Column(String(60), nullable=False)
    org_contact_number = Column(String(30), nullable=False)
    status = Column(String(30), nullable=False)
    customer_account_id = Column(Integer, ForeignKey('customer_account.id'))

    # Relationship to CustomerAccount
    customer_account = relationship("CustomerAccount", back_populates="admin_entry")

class account_reg(Base):
    __tablename__ = "account_reg"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), nullable=False)
    password = Column(String(60), nullable=False)

    employee = relationship("employee_reg_acc", back_populates="account")
    customers = relationship("CustomerAccount", back_populates="account")

class employee_reg_acc(Base):
    __tablename__ = "employee_reg_acc"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    job_title = Column(String(60), nullable=False)
    department = Column(String(60), nullable=False)
    gender = Column(String(30), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    marital_status = Column(String(30), nullable=False)
    email = Column(String(120), nullable=False)
    contact_number = Column(String(30), nullable=False)
    street_address = Column(String(120), nullable=False)
    city = Column(String(60), nullable=False)
    state = Column(String(40), nullable=False)
    postcode = Column(String(40), nullable=False)
    country = Column(String(60), nullable=False)
    employee_id = Column(Integer, ForeignKey(
        'account_reg.id', ondelete="CASCADE"), nullable=False)

    account = relationship("account_reg", back_populates="employee")


# Customer models
class MyEnum(enum.Enum):
    business = "business"
    education = "education"
    event = "event"
    others = "others"

class CustomerAccount(Base):
    __tablename__ = 'customer_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_name = Column(String(100), nullable=False)
    submission_date = Column(DateTime, default=datetime.now)
    ssm_number = Column(String(60), nullable=False)
    email_address = Column(String(350), nullable=False)
    contact_number = Column(String(15), nullable=False)
    street_address = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    postcode = Column(Integer, nullable=False)
    country = Column(String(50), nullable=False)
    purpose = Column(Enum(MyEnum), nullable=False)
    approval_status = Column(Boolean, default=False)
    account_id = Column(Integer, ForeignKey('account_reg.id', ondelete="CASCADE"), nullable=False)

    account = relationship("account_reg", back_populates="customers")
    admin_entry = relationship("admin_page", back_populates="customer_account", uselist=False)