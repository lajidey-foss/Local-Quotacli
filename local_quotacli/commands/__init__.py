# Copyright (c) 2025, oasyx dev and Contributors
# License: MIT. See LICENSE

import cProfile
import pstats
import subprocess  # nosec
import sys
from functools import wraps
from io import StringIO
from os import environ

import click

import frappe
import frappe.utils

click.disable_unicode_literals_warning = True

# end and begin
# begin end
""" def call_command(cmd, context):
	return click.Context(cmd, obj=context).forward(cmd) """


def get_commands():
	# prevent circular imports
	from .app_clicks import commands as app_commands

	clickable_link = "https://frappeframework.com/docs"
	all_commands = (
		app_commands
	)

	for command in all_commands:
		if not command.help:
			command.help = f"Refer to {clickable_link}"

	return all_commands


commands = get_commands()
