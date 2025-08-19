import frappe
from frappe.installer import update_site_config
from frappe.utils.data import add_days, add_years, today, get_year_ending, get_date_str

def before_install():    
    #fy_list = frappe.get_doc
    fy = frappe.get_value("Fiscal Year", {'disabled': 0}, "year_end_date")

    data = {
        'valid_till': add_days(today(), 15),
        'periodfy': get_date_str(fy),
        'document_limit': {
            'Sales Invoice': {'limit': 1000, 'period': 'Daily'},
            'Purchase Invoice': {'limit': 100, 'period': 'Weekly'},
            'Journal Entry': {'limit': 100, 'period': 'Monthly'},
            'Payment Entry': {'limit': 1000, 'period': 'Monthly'}
        }
    }
    # Updating site config
    # print (f"before => \n\n {get_date_str(get_year_ending(today()))}")
    update_site_config('allot', data)
