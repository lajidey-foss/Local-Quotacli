import frappe
from frappe.installer import update_site_config
from frappe.utils.data import add_days, today, get_date_str
from uuid import uuid4

def before_install():    
    fy = frappe.get_value("Fiscal Year", {'disabled': 0}, "year_end_date")
    token = str(uuid4())

    data = {
        'valid_till': add_days(today(), 15),
        'token_key': token,
        'periodfy': get_date_str(fy),
        'document_limit': {
            'Sales Invoice': {'limit': 1000, 'period': 'Daily'},
            'Purchase Invoice': {'limit': 100, 'period': 'Weekly'},
            'Journal Entry': {'limit': 100, 'period': 'Monthly'},
            'Payment Entry': {'limit': 1000, 'period': 'Monthly'}
        }
    }
    # Updating site config
    update_site_config('allot', data)
    print (f"installing ==> {token}")
