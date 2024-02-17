import datetime
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from database import models
import api.system.opt_locking.opt_locking as opt_locking
from security.system.authorization import Grant
import logging
from datetime import date
import safrs
import json
import requests
from confluent_kafka import Producer, KafkaException
from config.config import Args
import socket

app_logger = logging.getLogger(__name__)

declare_logic_message = "ALERT:  *** No Rules Yet ***"  # printed in api_logic_server.py
db = safrs.DB 
session = db.session 
producer = None
conf = None
    
def declare_logic():
    ''' Declarative multi-table derivations and constraints, extensible with Python. 

    Brief background: see readme_declare_logic.md
    
    Use code completion (Rule.) to declare rules here:
    '''
    
    def handle_all(logic_row: LogicRow):  # OPTIMISTIC LOCKING, [TIME / DATE STAMPING]
        """
        This is generic - executed for all classes.

        Invokes optimistic locking.

        You can optionally do time and date stamping here, as shown below.

        Args:
            logic_row (LogicRow): from LogicBank - old/new row, state
        """
        global producer,conf
        if Args.instance.kafka_producer:
            conf = Args.instance.kafka_producer
            if "client.id" not in conf:
                conf["client.id"] = socket.gethostname()
            # conf = {'bootstrap.servers': 'localhost:9092', 'client.id': socket.gethostname()}
            producer = Producer(conf)
            app_logger.debug(f'\nKafka producer connected')
        
        #This will enable declarative role based access 
        Grant.process_updates(logic_row=logic_row)
        
        if logic_row.is_updated() and logic_row.old_row is not None and logic_row.nest_level == 0:
            opt_locking.opt_lock_patch(logic_row=logic_row)
        
        enable_creation_stamping = True  # OpenDate time stamping
        if enable_creation_stamping:
            row = logic_row.row
            if logic_row.ins_upd_dlt == "ins" and hasattr(row, "OpenDate"):
                row.OpenDate = datetime.datetime.now()
                logic_row.log("early_row_event_all_classes - handle_all sets 'OpenDate"'')
        
    Rule.early_row_event_all_classes(early_row_event_all_classes=handle_all)
    
    Rule.sum(derive=models.Account.AcctBalance, 
                as_sum_of=models.Transaction.TotalAmount)
    
    Rule.constraint(validate=models.Account, 
                as_condition=lambda row: row.AcctBalance >= 0,
                error_msg="Account balance {row.AcctBalance} cannot be less than zero")
        
    Rule.formula(derive=models.Transaction.TotalAmount,
                as_expression=lambda row: row.Deposit - row.Withdrawl)
    
    Rule.constraint(validate=models.Transaction, 
                as_condition=lambda row: row.Deposit >= 0,
                error_msg="Deposit {row.Deposit} must be a positive amount")
    
    Rule.constraint(validate=models.Transaction, 
                as_condition=lambda row: row.Withdrawl >= 0,
                error_msg="Withdrawl {row.Withdrawl} must be a positive amount")
    
    Rule.constraint(validate=models.Transfer, 
                as_condition=lambda row: row.FromAccountID != row.ToAccountID,
                error_msg="FromAccount {row.FromAccountID} must be different from ToAccount {row.ToAccountID}")
            
    def fn_overdraft(row=models.Account, old_row=models.Account, logic_row=LogicRow):
        if row.AcctBalance  < 0: #  __lt__(0):
            pass
            # Find and transfer funds from "Loan"
            #1) find loan account if exists
            #2) if loanAcct.AcctBalance > overdraft then transfer funds
    
    Rule.commit_row_event(on_class=models.Account,calling=fn_overdraft)
    
    def fn_default_customer(row=models.Customer , old_row=models.Customer, logic_row=LogicRow):
        if logic_row.ins_upd_dlt == "ins" and row.RegistrationDate is None:
            row.RegistrationDate = date.today()
        
    def fn_default_account(row=models.Account, old_row=models.Account, logic_row=LogicRow):
        if logic_row.ins_upd_dlt == "ins":
            if row.AcctBalance is None:
                row.AcctBalance = 0
            if row.OpenDate is None:
                row.OpenDate = date.today()
        
    def fn_default_transaction(row=models.Transaction, old_row=models.Transaction, logic_row=LogicRow):
        if logic_row.ins_upd_dlt == "ins":
            if row.TotalAmount is None:
                row.TotalAmount = 0
            if row.Deposit is None:
                row.Deposit = 0
            if row.Withdrawl is None:
                row.Withdrawl = 0
            if row.TransactionDate is None:
                row.TransactionDate = date.today()

    def fn_default_transfer(row=models.Transfer, old_row=models.Transfer, logic_row=LogicRow):
        if logic_row.ins_upd_dlt == "ins" and row.TransactionDate is None:
                row.TransactionDate = date.today()
    
    def fn_transfer_funds(row=models.Transfer, old_row=models.Transfer, logic_row=LogicRow):
        if logic_row.ins_upd_dlt != "ins":
            return
        fromAcctId = row.FromAccountID
        toAcctId = row.ToAccountID
        amount = row.Amount
        
        transactions = session.query(models.Transaction).all()
        try:
            from_account = session.query(models.Account).filter(models.Account.AccountID == fromAcctId).one()
        except Exception as ex:
            raise requests.RequestException(
                f"From Account {fromAcctId} not found"
            ) from ex
            
        try:
            to_account = session.query(models.Account).filter(models.Account.AccountID == toAcctId).one()
        except Exception as ex:
            raise requests.RequestException(
                f"To Account {toAcctId} not found"
            ) from ex
        
        if from_account.Customer != to_account.Customer:
            raise requests.RequestException(
                f"FromAccount Customer {from_account.Customer} must be the same as the ToAccount Customer {to_account.Customer}"
            ) from ex
        
        if from_account.AcctBalance > amount:
            # #Not Enough Funds - if Loan exists move to cover Overdraft (transfer Loan to from_acct)
            pass
            
        from_trans = models.Transaction()
        from_trans.TransactionID = len(transactions) + 2
        from_trans.AccountID = fromAcctId
        from_trans.Withdrawl = amount
        from_trans.TransactionType = "Transfer"
        from_trans.TransactionDate = date.today()
        session.add(from_trans)
        
        to_trans = models.Transaction()
        to_trans.TransactionID = len(transactions) + 3
        to_trans.AccountID = toAcctId
        to_trans.Deposit = amount
        to_trans.TransactionType = "Transfer"
        to_trans.TransactionDate = date.today()
        session.add(to_trans)
        
        if producer:
            try:
                value = {
                    "transactionID": row.TransactionID,
                    "transactionDate": date.today(),
                    "customerID": to_account.CustomerID,
                    "fromAcct": fromAcctId,
                    "toAcct": toAcctId,
                    "amount": amount
                }
                producer.produce(value=value, topic="transfer_funds", key=row.TransactionID)
            except KafkaException as ke:
                logic_row.log("kafka_producer#kafka_message error: {ke}") 
        
        logic_row.log("Funds transferred successfully!")

    Rule.early_row_event(on_class=models.Customer, calling=fn_default_customer)
    Rule.early_row_event(on_class=models.Account, calling=fn_default_account)
    Rule.early_row_event(on_class=models.Transaction, calling=fn_default_transaction)
    Rule.early_row_event(on_class=models.Transfer, calling=fn_default_transfer)

    Rule.commit_row_event(on_class=models.Transfer, calling=fn_transfer_funds)

    declare_logic_message = "..logic/declare_logic.py (logic == rules + code)"
    app_logger.debug("..logic/declare_logic.py (logic == rules + code)")

