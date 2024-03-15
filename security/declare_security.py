from security.system.authorization import Grant, Security, DefaultRolePermission, GlobalFilter
import logging
from database import models
import safrs

db = safrs.DB
session = db.session

app_logger = logging.getLogger(__name__)

declare_security_message = "No Grants Yet"  # printed in api_logic_server.py

"""
Declare Security here, for example:

class Roles():
    ''' Define Roles here, so can use code completion (Roles.tenant) '''
    tenant = "tenant"
    renter = "renter"

Grant(  on_entity = models.Category,    # illustrate multi-tenant
        to_role = Roles.tenant,
        filter = lambda : models.Category.Client_id == Security.current_user().client_id)  # User table attributes

See [documentation](https://apilogicserver.github.io/Docs/Security-Overview/)

Security is invoked on server start (api_logic_server_run), per activation in `config.py`
"""
class Roles():
    manager = "manager"
    teller = "teller"
    customer = "customer"
    read_only = "readonly"
    admin = "CS_ADMIN"
    
#GlobalFilter(global_filter_attribute_name="CustomerID",roles_not_filtered=["admin"], filter= '{entity_class}.CustomerId = Security.current_user().CustomerID')

DefaultRolePermission(to_role=Roles.admin, can_read=True, can_insert=True,can_update=True, can_delete=True)
DefaultRolePermission(to_role=Roles.manager, can_read=True, can_insert=True,can_update=True, can_delete=False)
DefaultRolePermission(to_role=Roles.teller, can_read=True, can_insert=True,can_update=True, can_delete=False)
DefaultRolePermission(to_role=Roles.customer, can_read=True, can_insert=True,can_update=True, can_delete=False)
DefaultRolePermission(to_role=Roles.read_only, can_read=True, can_insert=False,can_update=False, can_delete=False)


#Grant(on_entity=models.Customer, to_role=Roles.customer, filter=lambda row: Security.current_user().CustomerID )
Grant(on_entity=models.Account, to_role=Roles.customer)
Grant(on_entity=models.Transaction, to_role=Roles.customer)