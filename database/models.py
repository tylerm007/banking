# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, Enum, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  February 17, 2024 13:11:51
# Database: mysql+pymysql://root:p@localhost:3306/banking
# Dialect:  mysql
#
# mypy: ignore-errors
########################################################################################################################

from safrs import SAFRSBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.mysql import *



class AccountType(SAFRSBase, Base):
    __tablename__ = 'AccountType'
    _s_collection_name = 'AccountType'  # type: ignore
    __bind_key__ = 'None'

    Name = Column(String(25), primary_key=True)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    AccountList : Mapped[List["Account"]] = relationship(back_populates="AccountType1")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Branch(SAFRSBase, Base):
    __tablename__ = 'Branch'
    _s_collection_name = 'Branch'  # type: ignore
    __bind_key__ = 'None'

    OFFICEID = Column("BranchID",Integer, primary_key=True)
    NAME = Column("Name",String(100))
    Office = Column(String(15))
    ADDRESS = Column("Address", String(100))
    STARTDATE = Column("OpenDate", DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    CustomerList : Mapped[List["Customer"]] = relationship(back_populates="Branch")
    EmployeeList : Mapped[List["Employee"]] = relationship(back_populates="Branch1")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Customer(SAFRSBase, Base):
    __tablename__ = 'Customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'
    #"CUSTOMERID","NAME","SURNAME","ADDRESS","STARTDATE","EMAIL","CUSTOMERTYPEID"
    CUSTOMERID = Column("CustomerID", Integer, primary_key=True)
    NAME = Column("FirstName", String(50))
    SURNAME = Column("LastName", String(50))
    EMAIL = Column("Email", String(100))
    PhoneNumber = Column(String(20))
    Address = Column(String(200))
    STARTDATE = Column("BirthDate",Date, server_default="CURRENT_DATE")
    RegistrationDate = Column(DateTime)
    UserName = Column(String(64))
    Password = Column(String(64))
    BranchID = Column(ForeignKey('Branch.BranchID'), index=True)

    # parent relationships (access parent)
    Branch : Mapped["Branch"] = relationship(back_populates=("CustomerList"))

    # child relationships (access children)
    AccountList : Mapped[List["Account"]] = relationship(back_populates="Customer")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Employee(SAFRSBase, Base):
    __tablename__ = 'Employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'
    #{"OFFICEID":5},"columns":["EMPLOYEEID","EMPLOYEENAME","EMPLOYEESURNAME","EMPLOYEEADDRESS","EMPLOYEESTARTDATE","EMPLOYEEEMAIL"]
    EMPLOYEEID = Column("EmployeeID", Integer, primary_key=True)
    EMPLOYEESURNAME = Column("LastName", String(15), nullable=False)
    EMPLOYEENAME = Column("FirstName", String(15), nullable=False)
    OFFICEID = Column("Branch", ForeignKey('Branch.BranchID'), server_default=text("'1'"), index=True)
    BirthDate = Column(DateTime)
    Photo = Column(String(25))
    EMPLOYEEEMAIL = Column("Notes", String(1024))

    # parent relationships (access parent)
    Branch1 : Mapped["Branch"] = relationship(back_populates=("EmployeeList"))

    # child relationships (access children)

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Account(SAFRSBase, Base):
    __tablename__ = 'Account'
    _s_collection_name = 'Account'  # type: ignore
    __bind_key__ = 'None'

    ACCOUNTTYPEID = Column("AccountID", Integer, primary_key=True)
    CustomerID = Column(ForeignKey('Customer.CustomerID'), index=True)
    ACCOUNTTYPENAME = Column("AccountType", ForeignKey('AccountType.Name'), index=True)
    AMOUNT : DECIMAL = Column("AcctBalance", DECIMAL(15, 2), server_default="0")
    OpenDate = Column(DateTime)

    # parent relationships (access parent)
    AccountType1 : Mapped["AccountType"] = relationship(back_populates=("AccountList"))
    Customer : Mapped["Customer"] = relationship(back_populates=("AccountList"))

    # child relationships (access children)
    TransactionList : Mapped[List["Transaction"]] = relationship(back_populates="Account")
    TransferList : Mapped[List["Transfer"]] = relationship(foreign_keys='[Transfer.FromAccountID]', back_populates="Account")
    TransferList1 : Mapped[List["Transfer"]] = relationship(foreign_keys='[Transfer.ToAccountID]', back_populates="Account1")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Transaction(SAFRSBase, Base):
    __tablename__ = 'Transaction'
    _s_collection_name = 'Transaction'  # type: ignore
    __bind_key__ = 'None'

    TransactionID = Column(Integer, primary_key=True)
    AccountID = Column(ForeignKey('Account.AccountID'), index=True)
    TransactionType = Column(Enum('Deposit', 'Withdrawal', 'Transfer'))
    TotalAmount : DECIMAL = Column(DECIMAL(15, 2), server_default="0")
    Deposit : DECIMAL = Column(DECIMAL(15, 2), server_default="0")
    Withdrawl : DECIMAL = Column(DECIMAL(15, 2), server_default="0")
    ItemImage = Column(Text)
    TransactionDate = Column(DateTime)

    # parent relationships (access parent)
    Account : Mapped["Account"] = relationship(back_populates=("TransactionList"))

    # child relationships (access children)

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Transfer(SAFRSBase, Base):
    __tablename__ = 'Transfer'
    _s_collection_name = 'Transfer'  # type: ignore
    __bind_key__ = 'None'

    TransactionID = Column(Integer, primary_key=True)
    FromAccountID = Column(ForeignKey('Account.AccountID'), index=True)
    ToAccountID = Column(ForeignKey('Account.AccountID'), index=True)
    Amount : DECIMAL = Column(DECIMAL(15, 2), server_default="0")
    TransactionDate = Column(DateTime)

    # parent relationships (access parent)
    Account : Mapped["Account"] = relationship(foreign_keys='[Transfer.FromAccountID]', back_populates=("TransferList"))
    Account1 : Mapped["Account"] = relationship(foreign_keys='[Transfer.ToAccountID]', back_populates=("TransferList1"))

    # child relationships (access children)

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_
