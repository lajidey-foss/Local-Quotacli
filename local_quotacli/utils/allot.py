import frappe
from frappe import _
from frappe.utils import cint, get_first_day, get_first_day_of_week, getdate

# How to find the start of each limit period, given today's date
PERIOD_START = {
    "Daily": lambda d: d,
    "Weekly": get_first_day_of_week,
    "Monthly": get_first_day,
}

EXEMPT_USERS = ("Administrator", "Guest")


def get_allot() -> dict:
    """Return the `allot` block of site_config, or {} if it isn't there."""
    return frappe.get_site_config().get("allot") or {}


def newfy_limit(doc, method=None):
    """Block creating or extending a Fiscal Year beyond the activated period."""
    allowed = get_allot().get("periodfy")
    if not allowed:
        return

    # Only check when it matters: new FY, or the end date was changed
    if not (doc.is_new() or doc.has_value_changed("year_end_date")):
        return

    if getdate(doc.year_end_date) > getdate(allowed):
        frappe.throw(
            _(
                "Yearly activation is needed before you can add a new Fiscal Year "
                "period. Please contact your Administrator to activate the new period."
            ),
            title=_("Period Not Activated"),
        )


def user_limit(doc, method=None):
    """Cap the number of enabled System Users."""
    max_users = cint(get_allot().get("user_limit"))
    if not max_users:
        return  # not configured, nothing to enforce

    # Only users that would count toward the cap matter
    if doc.name in EXEMPT_USERS or not doc.enabled or doc.user_type != "System User":
        return

    # For existing users, only check when they become enabled / a System User
    if not doc.is_new() and not (
        doc.has_value_changed("enabled") or doc.has_value_changed("user_type")
    ):
        return

    active = frappe.db.count(
        "User",
        {
            "enabled": 1,
            "user_type": "System User",
            "name": ["not in", EXEMPT_USERS],
        },
    )

    if active >= max_users:
        frappe.throw(
            _("You have reached your limit of {0} active users. Please contact your Administrator to increase it.").format(max_users),
            title=_("User Limit"),
        )

def document_limit(doc, method=None):
    """Enforce the per-period creation quota for doctypes listed in document_limit."""
    rule = (get_allot().get("document_limit") or {}).get(doc.doctype)
    if not rule:
        return

    start_of = PERIOD_START.get(rule.get("period"))
    if not start_of:
        return  # unknown period name in config, nothing to enforce

    max_docs = cint(rule.get("limit"))
    start = start_of(getdate())

    # Everything created since the period start (nothing can be created in the future)
    usage = frappe.db.count(doc.doctype, {"creation": [">=", start]})

    if usage >= max_docs:
        frappe.throw(
            _("You have reached your {0} {1} limit of {2} and cannot create new documents. Please contact your Administrator.").format(
                _(doc.doctype), _(rule.get("period")), max_docs
            ),
            title=_("Quota Limit"),
        )