import hmac

import click
import frappe
from frappe.commands import get_site, pass_context
from frappe.installer import update_site_config
from frappe.utils import get_date_str
from local_quotacli.utils.reach import hash_token


@click.command("period-migrate")
@click.argument("value")
@click.option("--key", prompt=True, hide_input=True)
@pass_context
def period_migrate(context, value, key):

	click.echo(f"=====================>\n {context}")
    site = get_site(context)
    frappe.init(site)

    allot = (frappe.get_site_config() or {}).get("allot")
    if not allot or "token_key" not in allot:
        click.secho("Allot config not found on this site", fg="red")
        raise click.exceptions.Exit(1)

    if not hmac.compare_digest(hash_token(key), allot["token_key"]):
        click.secho("Invalid key", fg="red")
        raise click.exceptions.Exit(1)

	click.secho("========================>", fg="yellow", )

    allot["periodfy"] = get_date_str(value)
    update_site_config("allot", allot)

    click.secho(f"periodfy updated to {allot['periodfy']}", fg="green")
    frappe.destroy()


commands = [
    period_migrate,
]