import frappe
from frappe import _
from frappe.installer import update_site_config
from frappe.utils import get_first_day, get_first_day_of_week, getdate

# FY 
def newfy_limit(doc, event):
    # fy
    allot = frappe.get_site_config()['allot']
    allowed_fys = allot.get('periodfy')

    period = doc.year_end_date
    if period > allowed_fys:
        msg = _(f"Yearly Activation needed before you proceed to add new FY Period. Please connect or contact your Administrator to activate new period.")
        frappe.throw(msg, title="Period not Activated")



def document_limit(doc, event):
    """
    We check for the doctype in document_limit and compute accordingly.
    """
    limit_dict = frappe.get_site_config()['allot']['document_limit']
    if (limit_dict.get(doc.doctype)):
        limit = frappe._dict(limit_dict.get(doc.doctype))
        limit_period = get_limit_period(limit.period)
        usage = len(frappe.db.get_all(
            doc.doctype,
            filters={
                'creation': ['BETWEEN', [str(limit_period.start) + ' 00:00:00.000000', str(limit_period.end) + ' 23:59:59.999999']]
            }))
        if usage >= limit.limit:
            msg = _(f"Your have reached your {doc.doctype} {limit.period} limit of {limit.limit} and hench cannot create new document. Please contact administrator.")
            frappe.throw(msg, title="Quota Limit")


def get_limit_period(period):
    """
        Get date mappinf for document limit period
    """
    today = getdate()
    week_start = get_first_day_of_week(today)
    periods = {
        'Daily': {'start': str(today), 'end': str(today)},
        'Weekly': {'start': str(week_start), 'end': str(today)},
        'Monthly': {'start': str(get_first_day(today)), 'end': str(today)},
    }
    return frappe._dict(periods.get(period))