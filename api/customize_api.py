import logging
import util
import safrs
from flask import request, jsonify
from safrs import jsonapi_rpc
from database import models
import json
from sqlalchemy import text, select, update, insert, delete
from sqlalchemy.orm import load_only
import sqlalchemy
import requests
from datetime import date

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

app_logger = logging.getLogger(__name__)

db = safrs.DB 
session = db.session 

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

    api_map = {
        "employees": models.Employee,
        "customers": models.Customer,
        "branches": models.Branch,
        "accounts": models.Account,
        "transaction": models.Transaction
    }
    #https://try.imatia.com/ontimizeweb/services/qsallcomponents-jee/services/rest/customers/customerType/search
    @app.route("/services/rest/<path:path>", methods=['POST','PUT','DELETE'])
    def api_search(path):
        s = path.split("/")
        clz_name = s[0]
        clz_type = s[1] #[2] TODO customerType search advancedSearch (photo)
        api_clz = api_map.get(clz_name)
        payload = json.loads(request.data)
        filter, columns, sqltypes, offset, pagesize, orderBy, data = parsePayload(payload)
        method = request.method
        rows = []
        if method == 'PUT':
            stmt = update(api_clz).where(text(filter)).values(data)
            
        if method == 'DELETE':
            stmt = delete(api_clz).where(text(filter))
            
        if method == 'POST':
            if data != None:
                #this is an insert
                stmt = insert(api_clz).values(data)
                
            else:
                #GET (sent as POST)
                rows = get_rows_by_query(api_clz, filter, orderBy, columns, pagesize, offset)
                return jsonify(rows)
                
        session.execute(stmt)
        session.commit()
        return jsonify({f"{method}":True})


    def get_rows(api_clz, filter, order_by, columns, pagesize, offset):
        # New Style
        stmt = select(api_clz)
        if filter:
            stmt = stmt.where(text(filter))
        if order_by:
            stmt = stmt.order_by(parseOrderBy(order_by))
        # .options(load_only(list of columns))\ #TODO
        stmt = stmt.limit(pagesize).offset(offset)
        
        return stmt
    
    def get_rows_by_query(api_clz, filter, orderBy, columns, pagesize, offset):
        #Old Style
        rows = []
        results = session.query(api_clz) # or list of columns?
                    
        if columns:
            #stmt = select(api_clz).options(load_only(Book.title, Book.summary))
            pass #TODO
        
        if orderBy:
            results = results.order_by(text(parseOrderBy(orderBy)))

        if filter:
            results = results.filter(text(filter)) 
            
        results = results.limit(pagesize) \
            .offset(offset) 
        
        for row in results.all():
            rows.append(row.to_dict())
        
        return rows
                    
    def parsePayload(payload:str):
        """
            employee/advancedSearch
            {"filter":{},"columns":["EMPLOYEEID","EMPLOYEETYPEID","EMPLOYEENAME","EMPLOYEESURNAME","EMPLOYEEADDRESS","EMPLOYEESTARTDATE","EMPLOYEEEMAIL","OFFICEID","EMPLOYEEPHOTO","EMPLOYEEPHONE"],"sqltypes":{},"offset":0,"pageSize":16,"orderBy":[]}
            customers/customer/advancedSearch
            {"filter":{},"columns":["CUSTOMERID","NAME","SURNAME","ADDRESS","STARTDATE","EMAIL"],"sqltypes":{"STARTDATE":93},"offset":0,"pageSize":25,"orderBy":[{"columnName":"SURNAME","ascendent":true}]}
            
        """
        filter:dict = parseFilter(payload.get('filter', {}))
        columns:list = payload.get('columns') or []
        sqltypes = payload.get('sqltypes') or None
        offset:int = payload.get('offset') or 0
        pagesize:int = payload.get('pageSize') or 25
        orderBy:list = payload.get('orderBy') or []
        data = payload.get('data',None)
        
        print(filter, columns, sqltypes, offset, pagesize, orderBy, data)
        return filter, columns, sqltypes, offset, pagesize, orderBy, data
    
    def parseFilter(filter:dict) -> str:
        # {filter":{"@basic_expression":{"lop":"BALANCE","op":"<=","rop":35000}}
        filter_result = ""
        a = ""
        for f in filter:
            if f == '@basic_expression':
                continue
            filter_result += f"{a} {f} = {filter[f]}"
            a = " and "
        return None if filter_result == "" else filter_result
        
    def parseData(data:dict = None) -> str:
        # convert dict to str
        result = ""
        join = ""
        if data:
            for d in data:
                result += f'{join}{d}="{data[d]}"'
                join = ","
        return result
    
    def parseOrderBy(orderBy) -> str:
        #[{'columnName': 'SURNAME', 'ascendent': True}]
        result = ""
        if orderBy and len(orderBy) > 0:
            result = f"{orderBy[0]['columnName']}" #TODO for desc
        return result
    
def rows_to_dict(result: any) -> list:
    """
    Converts SQLAlchemy result (mapped or raw) to dict array of un-nested rows

    Args:
        result (object): list of serializable objects (e.g., dict)

    Returns:
        list of rows as dicts
    """
    rows = []
    for each_row in result:
        row_as_dict = {}
        print(f'type(each_row): {type(each_row)}')
        if isinstance (each_row, sqlalchemy.engine.row.Row):  # raw sql, eg, sample catsql
            key_to_index = each_row._key_to_index             # note: SQLAlchemy 2 specific
            for name, value in key_to_index.items():
                row_as_dict[name] = each_row[value]
        else:
            row_as_dict = each_row.to_dict()                  # safrs helper
        rows.append(row_as_dict)
    return rows

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