import frappe
from frappe.installer import update_site_config
from frappe.utils.data import add_days, add_years, today, get_year_ending

def before_install():
    filters = {
        'enabled': 1,
        'name': ['not in', ['Guest', 'Administrator']]
    }
    # skipping number of users
    user_list = frappe.get_all('User', filters=filters, fields=["name"])

    active_users = 0

    for user in user_list:
        roles = frappe.get_all(
            "Has Role",
            filters={
                'parent': user.name
            },
            fields=['role']
        )

        for row in roles:
            if frappe.get_value("Role", row.role, "desk_access") == 1:
                active_users += 1
                break
    
    #trials = add_years(today(), 1)
    data = {
        'users': 20,
        'active_users': active_users,
        'company': 2,
        'used_company':1,
        'count_website_users': 0,
        'count_administrator_user': 0,
        'valid_till': add_days(today(), 15),
        'allot_fy_valid': get_year_ending(today()),
        'document_limit': {
            'Sales Invoice': {'limit': 1000, 'period': 'Daily'},
            'Purchase Invoice': {'limit': 100, 'period': 'Weekly'},
            'Journal Entry': {'limit': 100, 'period': 'Monthly'},
            'Payment Entry': {'limit': 1000, 'period': 'Monthly'}
        }
    }
    # Updating site config
    update_site_config('allot', data)

    #SELECT name, year, year_start_date, year_end_date  FROM `tabFiscal Year`  WHERE YEAR(year_end_date) = YEAR(CURRENT_DATE);
    