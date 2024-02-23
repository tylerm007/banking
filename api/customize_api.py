from functools import wraps
import logging
import yaml
from pathlib import Path
from flask_cors import cross_origin
import util
import safrs
from flask import request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from safrs import jsonapi_rpc
from database import models
import json
from sqlalchemy import text, select, update, insert, delete
from sqlalchemy.orm import load_only
import sqlalchemy
import requests
from datetime import date
from config.config import Args

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
    # sourcery skip: avoid-builtin-shadow
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
    def admin_required():
        """
        Support option to bypass security (see cats, below).

        See: https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators/
        """
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                if Args.security_enabled == False:
                    return fn(*args, **kwargs)
                verify_jwt_in_request(True)  # must be issued if security enabled
                #clientId = jwt[1].get('clientId', -1)
                return fn(*args, **kwargs)
            return decorator
        return wrapper
        user = request.args.get('user')
        return jsonify({"result": f'hello, {user}'})

    @app.route('/metadata')
    def metadata():
        """
        Swagger provides typical API discovery.  This is for tool providers
        requiring programmatic access to api definition, e.g., 
        to drive artifact code generation.

        Returns json for list of 1 / all resources, with optional attribute name/type, eg

        curl -X GET "http://localhost:5656/metadata?resource=Category&include=attributes"

        curl -X GET "http://localhost:5656/metadata?include=attributes"
        """

        resource_name = request.args.get('resource')
        include_attributes = False
        include = request.args.get('include')
        if include:
            include_attributes = "attributes" in include
        return jsonify(getMetaData(resource_name=resource_name, include_attributes=include_attributes))

    def getMetaData(resource_name:str = None, include_attributes: bool = True) -> dict:
        import inspect
        import sys
        resource_list = []  # array of attributes[], name (so, the name is last...)
        resource_objs = {}  # objects, named = resource_name

        models_name = "database.models"
        cls_members = inspect.getmembers(sys.modules["database.models"], inspect.isclass)
        for each_cls_member in cls_members:
            each_class_def_str = str(each_cls_member)
            if (f"'{models_name}." in each_class_def_str and
                            "Ab" not in each_class_def_str):
                each_resource_name = each_cls_member[0]
                each_resource_class = each_cls_member[1]
                each_resource_mapper = each_resource_class.__mapper__
                if resource_name is None or resource_name == each_resource_name:
                    resource_object = {"name": each_resource_name}
                    resource_list.append(resource_object)
                    resource_objs[each_resource_name] = {}
                    if include_attributes:
                        attr_list = []
                        for each_attr in each_resource_mapper.attrs:
                            if not each_attr._is_relationship:
                                try:
                                    attribute_object = {"name": each_attr.key,
                                                        "attr": each_attr,
                                                        "type": str(each_attr.expression.type)}
                                except Exception as ex:
                                    attribute_object = {"name": each_attr.key,
                                                        "exception": f"{ex}"}
                                attr_list.append(attribute_object)
                        resource_object["attributes"] = attr_list
                        resource_objs[each_resource_name] = {"attributes": attr_list}
        # pick the format you like
        #return_result = {"resources": resource_list}
        return_result = {"resources": resource_objs}
        return return_result
    
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

    @app.route("/branch", methods=['POST'])
    def branch():
        """
        curl -X 'POST' http://localhost:5656/branch -d @branch.json \     
            -H 'accept: application/vnd.api+json' \   
            -H 'Content-Type: application/vnd.api+json'       
        """
        payload = json.loads(request.data)
        branch_id = 5
        for branch_record in payload["data"]:
            clz = models.Branch()
            clz.Name = branch_record["Name"]
            clz.Address = branch_record["Address"]
            clz.Office = branch_record["Office"]
            clz.OpenDate = date.today()
            clz.BranchID = branch_id
            session.add(clz)
            branch_id = branch_id + 1
            session.commit()
        return jsonify(status=True)
    
    @app.route("/customer", methods=['POST'])
    def customer():
        """_summary_
        curl -X 'POST' http://localhost:5656/customer -d @customer.json \
            -H 'accept: application/vnd.api+json' \
            -H 'Content-Type: application/vnd.api+json'
        """
        payload = json.loads(request.data)
        for customer_record in payload["data"]:
            clz = models.Customer()
            clz.FirstName = customer_record["NAME"]
            clz.LastName = customer_record["SURNAME"]
            if "ADDRESS" in customer_record:
                clz.Address = customer_record["ADDRESS"]
            if "EMAIL" in customer_record:
                clz.Email = customer_record["EMAIL"]
            clz.RegistrationDate = date.today()
            clz.CustomerID = customer_record["CUSTOMERID"]
            clz.UserName = customer_record["NAME"]
            clz.Password = "password"
            session.add(clz)
            session.commit()
        return jsonify(status=True)
    
    @app.route("/employee", methods=['POST'])
    def employee():
        """_summary_
        curl -X 'POST' http://localhost:5656/employee -d @employee.json \
            -H 'accept: application/vnd.api+json' \
            -H 'Content-Type: application/vnd.api+json'
        """
        payload = json.loads(request.data)
        for customer_record in payload["data"]:
            clz = models.Employee()
            clz.FirstName = customer_record["EMPLOYEENAME"]
            clz.LastName = customer_record["EMPLOYEESURNAME"]
            if "EMPLOYEEADDRESS" in customer_record:
                clz.Address = customer_record["EMPLOYEEADDRESS"]
            if "EMPLOYEEEMAIL" in customer_record:
                clz.Email = customer_record["EMPLOYEEEMAIL"]
            if "EMPLOYEEPHONE" in customer_record:
                pass
            clz.BirthDate = date.today()
            clz.CustomerID = customer_record["EMPLOYEEID"]

            session.add(clz)
            session.commit()
        return jsonify(status=True)
    
    api_map = {
        "employees": models.Employee,
        "customers": models.Customer,
        "branches": models.Branch,
        "accounts": models.Account,
        "accounttypes": models.AccountType,
        "transactions": models.Transaction
    }
    # http://localhost:5656/ontimizeweb/services/qsallcomponents-jee/services/rest/customers/customerType/search
    #https://try.imatia.com/ontimizeweb/services/qsallcomponents-jee/services/rest/customers/customerType/search
    @app.route("/ontimizeweb/services/qsallcomponents-jee/services/rest/<path:path>", methods=['POST','PUT','PATCH','DELETE','OPTIONS'])
    @app.route("/services/rest/<path:path>", methods=['POST','PUT','PATCH','DELETE','OPTIONS'])
    @admin_required() 
    @cross_origin(vary_header=True)
    def api_search(path):
        s = path.split("/")
        clz_name = s[0]
        clz_type = s[1] #[2] TODO customerType search advancedSearch defer(photo)customerTypeAggregate
        api_clz = api_map.get(clz_name)
        method = request.method
        rows = []
        #CORS 
        if method == "OPTIONS":
            return jsonify(success=True)
        
        payload = json.loads(request.data)
        filter, columns, sqltypes, offset, pagesize, orderBy, data = parsePayload(payload)
        
        if method in ['PUT','PATCH']:
            stmt = update(api_clz).where(text(filter)).values(data)
            
        if method == 'DELETE':
            stmt = delete(api_clz).where(text(filter))
            
        if method == 'POST':
            if data != None:
                #this is an insert
                stmt = insert(api_clz).values(data)
            else:
                #GET (sent as POST)
                #rows = get_rows_by_query(api_clz, filter, orderBy, columns, pagesize, offset)
                if "TypeAggregate" in clz_type:
                    return get_rows_agg(request, api_clz, filter, columns)
                else:
                    return get_rows(request, api_clz,filter, orderBy, columns, pagesize, offset)
                
        session.execute(stmt)
        session.commit()
        return jsonify({f"{method}":True})

    def get_rows_agg(request: any, api_clz, filter, columns):
        from sqlalchemy import func
        resources = getMetaData(api_clz.__name__)
        attributes = resources["resources"][api_clz.__name__]["attributes"]
        list_of_columns = ""
        sep = ""
        attr_list = list(api_clz._s_columns)
        table_name = api_clz._s_type
        #api_clz.__mapper__.attrs #TODO map the columns to the attributes to build the select list
        for a in attributes:
            name = a["name"]
            t = a["type"] #INTEGER or VARCHAR(N)
            #list_of_columns.append(api_clz._sa_class_manager.get(n))
            attr = a["attr"]
            #MAY need to do upper case compares
            if name in columns:
                list_of_columns = f'{list_of_columns}{sep}{name}'
                sep = ","
        sql = f' count(*), {list_of_columns} from {table_name} group by {list_of_columns}'
        print(sql)
        #rows = session.query(text(sql)).all()
        rows = session.query(models.Account.ACCOUNTTYPEID,func.count(models.Account.AccountID)).group_by(models.Account.ACCOUNTTYPEID).all()
        return jsonify(rows)
    
    def get_rows(request: any, api_clz, filter, order_by, columns, pagesize, offset):
        # New Style
        key = api_clz.__name__.lower()
        resources = getMetaData(api_clz.__name__)
        attributes = resources["resources"][api_clz.__name__]["attributes"]
        list_of_columns = []
        for a in attributes:
            name = a["name"]
            t = a["type"] #INTEGER or VARCHAR(N)
            #MAY need to do upper case compares
            if name in columns:
                list_of_columns.append(name)
        print(list_of_columns)
        from api.system.custom_endpoint import CustomEndpoint
        request.method = 'GET'
        r = CustomEndpoint(model_class=api_clz, fields=list_of_columns, filter_by=filter)
        result = r.execute(request=request)
        return r.transform("IMATIA",key, result)
    
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
        sqltypes = payload.get('sqltypes') or None
        filter = parseFilter(payload.get('filter', {}),sqltypes)
        columns:list = payload.get('columns') or []
        offset:int = payload.get('offset') or 0
        pagesize:int = payload.get('pageSize') or 25
        orderBy:list = payload.get('orderBy') or []
        data = payload.get('data',None)
        
        print(filter, columns, sqltypes, offset, pagesize, orderBy, data)
        return filter, columns, sqltypes, offset, pagesize, orderBy, data
    
    def parseFilter(filter:dict,sqltypes: any) -> str:
        # {filter":{"@basic_expression":{"lop":"BALANCE","op":"<=","rop":35000}}
        filter_result = ""
        a = ""
        for f in filter:
            if f == '@basic_expression':
                continue
            q = "" if f == "OFFICEID" else "'" #TODO use sqltypes for name == a
            name = filter[f] #TODO f rename to internal column
            db_colname = "BranchID" if f == "OFFICEID" else f
            filter_result += f"{a} {db_colname} = {q}{name}{q}"
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
    @classmethod
    @jsonapi_rpc(http_methods=["POST"])
    def transfer(cls, *args, **kwargs):
        """ # yaml creates Swagger description
            args :
                CustomerId: 1
                FromAcctId: 8
                ToAcctId: 7 
                Amount: 10
        """
        db = safrs.DB         # Use the safrs.DB, not db!
        session = db.session  # sqlalchemy.orm.scoping.scoped_session
        
        jsonData = json.loads(request.data.decode('utf-8'))
        payload = DotDict(jsonData["meta"]['args'])
        customerId = payload.customer_id
        transactions = session.query(models.Transaction).all() #TODO where(CustomerID = N)
        try:
            from_account = session.query(models.Account).filter(models.Account.AccountID == payload.FromAcctId).one()
        except Exception as ex:
            raise requests.RequestException(
                f"From Account {payload.FromAcctId} not found"
            ) from ex
        from_trans = models.Transaction()
        from_trans.TransactionID = len(transactions) + 2
        from_trans.AccountID = payload.FromAcctId
        from_trans.Withdrawl = payload.Amount
        from_trans.TransactionType = "Withdrawal"
        from_trans.TransactionDate = date.today()
        session.add(from_trans)

        try:
            to_account = session.query(models.Account).filter(models.Account.AccountID == payload.ToAcctId).one()
        except Exception as ex:
            raise requests.RequestException(
                f"To Account {payload.ToAcctId} not found"
            ) from ex
            
        to_trans = models.Transaction()
        to_trans.TransactionID = len(transactions) + 3
        to_trans.AccountID = payload.ToAcctId
        to_trans.Deposit = payload.Amount
        to_trans.TransactionType = "Deposit"
        to_trans.TransactionDate = date.today()
        session.add(to_trans)
        session.commit()
        
        return {f"Transfer Completed amount: {payload.Amount} from acct: {payload.FromAcctId} to acct: {payload.ToAcctId}"} 