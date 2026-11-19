import hashlib
import frappe
from frappe.utils.data import add_days, today, get_date_str, get_year_ending

def get_fy_end():
    try:
        fy = frappe.get_value(
            "Fiscal Year",
            {
                "disabled": 0,
                "year_start_date": ["<=", today()],
                "year_end_date": [">=", today()],
            },
            "year_end_date",
        )
    except Exception:
        fy = None
    return fy or get_year_ending(today())

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()