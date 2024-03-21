# coding: utf-8
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  March 01, 2024 10:07:43
# Database: postgresql://demo:demouser@localhost/ontimize
# Dialect:  postgresql
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

from sqlalchemy.dialects.postgresql import *



class AccountType(SAFRSBase, Base):
    __tablename__ = 'AccountType'
    _s_collection_name = 'AccountType'  # type: ignore
    __bind_key__ = 'None'

    AcctID = Column(Integer, server_default=text("nextval('\"AccountType_AcctID_seq\"'::regclass)"), primary_key=True)
    NAME = Column(String(25), nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    AccountList : Mapped[List["Account"]] = relationship(back_populates="AccountType")

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

    OFFICEID = Column(Integer, primary_key=True)
    NAME = Column(String(100))
    ADDRESS = Column(String(100))
    STARTDATE = Column(Date)

    # parent relationships (access parent)

    # child relationships (access children)
    CustomerList : Mapped[List["Customer"]] = relationship(back_populates="Branch")
    EmployeeList : Mapped[List["Employee"]] = relationship(back_populates="Branch")
    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Movement(SAFRSBase, Base):
    __tablename__ = 'Movements'
    _s_collection_name = 'Movement'  # type: ignore
    __bind_key__ = 'None'

    MOVEMENTID = Column(Integer, server_default=text("0"), primary_key=True)
    ACCOUNTID = Column(Integer)
    MOVEMENTTYPEID = Column(Integer, server_default=text("1"))
    MOVEMENT = Column(Numeric(15, 2), server_default=text("0.00"))
    Deposit = Column(Numeric(15, 2), server_default=text("0.00"))
    Withdrawl = Column(Numeric(15, 2), server_default=text("0.00"))
    ItemImage = Column(Text)
    DATE_ = Column(Date)

    # parent relationships (access parent)

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


class Customer(SAFRSBase, Base):
    __tablename__ = 'Customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    CUSTOMERID = Column(Integer,  primary_key=True)
    NAME = Column(String(75))
    SURNAME = Column(String(75))
    EMAIL = Column(String(100))
    ADDRESS = Column(String(200))
    STARTDATE = Column(Date)
    OFFICEID = Column(ForeignKey('Branch.OFFICEID'), server_default=text("1"))
    PHOTO = Column(Text)

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

    EMPLOYEEID = Column(Integer, primary_key=True)
    EMPLOYEETYPEID = Column(Integer, server_default=text("1"))
    EMPLOYEESURNAME = Column(String(15), nullable=False)
    EMPLOYEENAME = Column(String(15), nullable=False)
    OFFICEID = Column(ForeignKey('Branch.OFFICEID'), server_default=text("1"))
    EMPLOYEEADDRESS = Column(String(100))
    EMPLOYEESTARTDATE = Column(Date, server_default=text("CURRENT_TIMESTAMP"))
    EMPLOYEEPHOTOTO = Column(Text)
    NAME = Column(String(100))
    EMPLOYEEPHONE = Column(String(50))

    # parent relationships (access parent)
    Branch : Mapped["Branch"] = relationship(back_populates=("EmployeeList"))

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

    ACCOUNTID = Column(Integer, primary_key=True)
    CUSTOMERID = Column(ForeignKey('Customer.CUSTOMERID'))
    ACCOUNTTYPEID = Column(ForeignKey('AccountType.AcctID'))
    ACCOUNTTYPENAME = Column(String(25))
    BALANCE = Column(Numeric(15, 2), default=0)
    STARTDATE = Column(Date)
    ENDDATE = Column(Date)
    ENTITYID = Column(Integer, server_default=text("1"))
    OFFICEID = Column(Integer, server_default=text("1"))
    CDID = Column(String(25))
    ANID = Column(String(25))
    INTERESRATE = Column(Numeric(15, 2), default=0)

    # parent relationships (access parent)
    AccountType : Mapped["AccountType"] = relationship(back_populates=("AccountList"))
    Customer : Mapped["Customer"] = relationship(back_populates=("AccountList"))

    # child relationships (access children)
    TransactionList : Mapped[List["Transaction"]] = relationship(back_populates="Account")
    TransferList : Mapped[List["Transfer"]] = relationship(foreign_keys='[Transfer.FromAccountID]', back_populates="FromAccount")
    TransferList1 : Mapped[List["Transfer"]] = relationship(foreign_keys='[Transfer.ToAccountID]', back_populates="ToAccount")

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
    AccountID = Column(ForeignKey('Account.ACCOUNTID'))
    TransactionType = Column(String(25), server_default=text("Deposit"))
    TotalAmount = Column(Numeric(15, 2), default=0)
    Deposit = Column(Numeric(15, 2), default=0)
    Withdrawl = Column(Numeric(15, 2), default=0)
    ItemImage = Column(Text)
    TransactionDate = Column(Date)

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
    FromAccountID = Column(ForeignKey('Account.ACCOUNTID'))
    ToAccountID = Column(ForeignKey('Account.ACCOUNTID'))
    Amount = Column(Numeric(15, 2), default=0)
    TransactionDate = Column(Date)

    # parent relationships (access parent)
    FromAccount : Mapped["Account"] = relationship(foreign_keys='[Transfer.FromAccountID]', back_populates=("TransferList"))
    ToAccount : Mapped["Account"] = relationship(foreign_keys='[Transfer.ToAccountID]', back_populates=("TransferList1"))

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
