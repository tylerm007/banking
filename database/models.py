# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, Enum, ForeignKey, Integer, LargeBinary, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  February 23, 2024 09:23:51
# Database: mysql+pymysql://root:password@127.0.0.1:3308/banking
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

    AcctID = Column(Integer, primary_key=True)
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
    STARTDATE = Column(DateTime)

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


class Customer(SAFRSBase, Base):
    __tablename__ = 'Customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    CUSTOMERID = Column(Integer, primary_key=True)
    NAME = Column(String(75))
    SURNAME = Column(String(75))
    EMAIL = Column(String(100))
    ADDRESS = Column(String(200))
    STARTDATE = Column(DateTime)
    BRANCHID = Column(ForeignKey('Branch.OFFICEID'), server_default=text("'1'"), index=True)

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
    EMPLOYEETYPEID = Column(Integer, server_default=text("'1'"))
    EMPLOYEESURNAME = Column(String(15), nullable=False)
    EMPLOYEENAME = Column(String(15), nullable=False)
    OFFICEID = Column(ForeignKey('Branch.OFFICEID'), server_default=text("'1'"), index=True)
    EMPLOYEEADDRESS = Column(String(100))
    EMPLOYEESTARTDATE = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    EMPLOYEEPHOTOTO = Column(LargeBinary)
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
    CUSTOMERID = Column(ForeignKey('Customer.CUSTOMERID'), index=True)
    ACCOUNTTYPEID = Column(ForeignKey('AccountType.AcctID'), index=True)
    ACCOUNTTYPENAME = Column(String(25))
    BALANCE : DECIMAL = Column(DECIMAL(15, 2), server_default=text("'0.00'"))
    STARTDATE = Column(DateTime)
    ENDDATE = Column(DateTime)
    ENTITYID = Column(Integer, server_default=text("'1'"))
    OFFICEID = Column(Integer, server_default=text("'1'"))
    CDID = Column(String(25))
    ANID = Column(String(25))
    INTERESRATE : DECIMAL = Column(DECIMAL(15, 2), server_default=text("'0.00'"))

    # parent relationships (access parent)
    AccountType : Mapped["AccountType"] = relationship(back_populates=("AccountList"))
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
    AccountID = Column(ForeignKey('Account.ACCOUNTID'), index=True)
    TransactionType = Column(Enum('Deposit', 'Withdrawal', 'Transfer'))
    TotalAmount : DECIMAL = Column(DECIMAL(15, 2), server_default=text("'0.00'"))
    Deposit : DECIMAL = Column(DECIMAL(15, 2), server_default=text("'0.00'"))
    Withdrawl : DECIMAL = Column(DECIMAL(15, 2), server_default=text("'0.00'"))
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
    FromAccountID = Column(ForeignKey('Account.ACCOUNTID'), index=True)
    ToAccountID = Column(ForeignKey('Account.ACCOUNTID'), index=True)
    Amount : DECIMAL = Column(DECIMAL(15, 2), server_default=text("'0.00'"))
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
