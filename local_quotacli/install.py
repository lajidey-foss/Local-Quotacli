import secrets

import click
import frappe
from frappe.installer import update_site_config
from frappe.utils.data import add_days, get_date_str, today

from local_quotacli.utils.reach import get_fy_end, hash_token


def before_install():
    allot = frappe.get_site_config().get("allot") or {}
    if allot.get("token_key"):
        click.secho("allot config already present, keeping existing token", fg="yellow")
        return

    fy = get_fy_end()
    token = secrets.token_urlsafe(32)

    data = {
        "valid_till": add_days(today(), 15),
        "token_key": hash_token(token),
        "periodfy": get_date_str(fy),
        "user_limit": 10,
        "document_limit": {
            "Sales Invoice": {"limit": 1000, "period": "Daily"},
            "Purchase Invoice": {"limit": 100, "period": "Weekly"},
            "Journal Entry": {"limit": 100, "period": "Monthly"},
            "Payment Entry": {"limit": 1000, "period": "Monthly"},
        },
    }
    update_site_config("allot", data)

    click.secho(f"installing ==> {token}", fg="yellow")