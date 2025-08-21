import json
import os

import click

import frappe
from frappe import _
from frappe.commands import get_site, pass_context
from frappe.exceptions import SiteNotSpecifiedError
from frappe.utils import cint, update_progress_bar


@click.command("period-migrate")
@click.argument("value")
@click.option('--key', prompt=True, hide_input=True)
@pass_context
def period_migrate(context, value, key):

	# check if key match else return
	click.echo(f"=====================>\n {context}")
	site_name = get_site(context)
	file_path = frappe.utils.get_bench_path()+ '/sites/' + \
		site_name+"/site_config.json"
	
	with open(file_path) as f:
		site_config = json.loads(f.read())
	
	validator = site_config['allot']['token_key']
	if not key == validator:
		return
	
	click.secho("========================>", fg="yellow", )
	value = frappe.utils.data.get_date_str(value)
	site_config['allot']["periodfy"] = value

	with open(file_path, "w") as f:
		f.write(json.dumps(site_config, indent=1, sort_keys=True))
	
	# to impliment udate_progress_bar use all data value from 
	# cli show-config
	# for each value length show 100% progress
	# or use cli version

commands = [
	period_migrate,
]