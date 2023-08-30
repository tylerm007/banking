import logging
import util
import safrs
from flask import request, jsonify
from safrs import jsonapi_rpc
from database import models
import json
import requests
from datetime import date

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

app_logger = logging.getLogger(__name__)
class DotDict(dict):
    """ dot.notation access to dictionary attributes """
    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
def expose_services(app, api, project_dir, swagger_host: str, PORT: str):
    """ Customize API - new end points for services 
    
        Brief background: see readme_customize_api.md
    
    """
    
    app_logger.debug("api/customize_api.py - expose custom services")

    api.expose_object(TransferFunds) 
    
    @app.route('/hello_world')
    def hello_world():  # test it with: http://localhost::5656/hello_world?user=ApiLogicServer
        """
        This is inserted to illustrate that APIs not limited to database objects, but are extensible.

        See: https://apilogicserver.github.io/Docs/API-Customize/

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """
        user = request.args.get('user')
        return jsonify({"result": f'hello, {user}'})


    @app.route('/stop')
    def stop():  # test it with: http://localhost:5656/stop?msg=API stop - Stop API Logic Server
        """
        Use this to stop the server from the Browser.

        See: https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """

        import os, signal

        msg = request.args.get('msg')
        app_logger.info(f'\nStopped server: {msg}\n')

        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({ "success": True, "message": "Server is shutting down..." })

class TransferFunds(safrs.JABase):
    """
    curl -X 'POST' \
        'http://localhost:5656/api/TransferFunds/transfer_funds' \
        -H 'accept: application/vnd.api+json' \
        -H 'Content-Type: application/json' \
        -d '{
        "meta": {
            "method": "transfer_funds",
            "args": {
            "customer_id": 1,
            "fromAcctId": 2000,
            "toAcctId": 1000,
            "amount": 10
            }
        }
        }'

    Args:
        safrs (_type_): _description_

    Raises:
        requests.RequestException: _description_

    Returns:
        _type_: "Transfer Completed...."
    """
    @classmethod
    @jsonapi_rpc(http_methods=["POST"])
    def transfer_funds(cls, *args, **kwargs):
        """ # yaml creates Swagger description
            args :
                customer_id: 1
                fromAcctId: 2000
                toAcctId: 1000 
                amount: 10
        """
        db = safrs.DB         # Use the safrs.DB, not db!
        session = db.session  # sqlalchemy.orm.scoping.scoped_session
        
        jsonData = json.loads(request.data.decode('utf-8'))
        payload = DotDict(jsonData["meta"]['args'])
        customerId = payload.customer_id
        transactions = session.query(models.Transaction).all()
        try:
            from_account = session.query(models.Account).filter(models.Account.AccountID == payload.fromAcctId).one()
        except Exception as ex:
            raise requests.RequestException(
                f"From Account {payload.fromAcctId} not found"
            ) from ex
        from_trans = models.Transaction()
        from_trans.TransactionID = len(transactions) + 1
        from_trans.AccountID = payload.fromAcctId
        from_trans.Withdrawl = payload.amount
        from_trans.TransactionType = "Transfer"
        from_trans.Deposit = 0
        from_trans.TotalAmount = 0
        from_trans.TransactionDate = date.today()
        session.add(from_trans)
        session.flush()
        try:
            to_account = session.query(models.Account).filter(models.Account.AccountID == payload.toAcctId).one()
        except Exception as ex:
            raise requests.RequestException(
                f"To Account {payload.toAcctId} not found"
            ) from ex
            
        to_trans = models.Transaction()
        to_trans.TransactionID = len(transactions) + 2
        to_trans.AccountID = payload.toAcctId
        to_trans.Deposit = payload.amount
        to_trans.TransactionType = "Transfer"
        to_trans.Withdrawl = 0
        to_trans.TotalAmount = 0
        to_trans.TransactionDate = date.today()
        session.add(to_trans)
        session.flush()
        
        session.commit()
        
        return {f"Transfer Completed amount: {payload.amount} from acct: {payload.fromAcctId} to acct: {payload.toAcctId}"} 