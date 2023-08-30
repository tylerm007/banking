# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  August 29, 2023 17:12:14
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



class Customer(SAFRSBase, Base):
    __tablename__ = 'Customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    CustomerID = Column(Integer, primary_key=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    Email = Column(String(100))
    PhoneNumber = Column(String(20))
    Address = Column(String(200))
    BirthDate = Column(Date)
    RegistrationDate = Column(DateTime)
    UserName = Column(String(64), nullable=False)
    Password = Column(String(64), nullable=False)
    allow_client_generated_ids = True

    # parent relationships (access parent)

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


class Account(SAFRSBase, Base):
    __tablename__ = 'Account'
    _s_collection_name = 'Account'  # type: ignore
    __bind_key__ = 'None'

    AccountID = Column(Integer, primary_key=True)
    CustomerID = Column(ForeignKey('Customer.CustomerID'), index=True)
    AccountType = Column(Enum('Savings', 'Checking', 'Loan'))
    AcctBalance : DECIMAL = Column(DECIMAL(15, 2))
    OpenDate = Column(DateTime)
    allow_client_generated_ids = True

    # parent relationships (access parent)
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
    TotalAmount : DECIMAL = Column(DECIMAL(15, 2))
    Deposit : DECIMAL = Column(DECIMAL(15, 2))
    Withdrawl : DECIMAL = Column(DECIMAL(15, 2))
    ItemImage = Column(Text)
    TransactionDate = Column(DateTime)
    allow_client_generated_ids = True

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
    Amount : DECIMAL = Column(DECIMAL(15, 2))
    TransactionDate = Column(DateTime)
    allow_client_generated_ids = True

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
