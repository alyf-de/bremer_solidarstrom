from . import __version__ as app_version

app_name = "bremer_solidarstrom"
app_title = "Bremer Solidarstrom"
app_publisher = "ALYF GmbH"
app_description = "ERPNext customizations for Bremer Solidarstrom"
app_email = "hallo@alyf.de"
app_license = "GPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bremer_solidarstrom/css/bremer_solidarstrom.css"
# app_include_js = "/assets/bremer_solidarstrom/js/bremer_solidarstrom.js"

# include js, css files in header of web template
# web_include_css = "/assets/bremer_solidarstrom/css/bremer_solidarstrom.css"
# web_include_js = "/assets/bremer_solidarstrom/js/bremer_solidarstrom.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bremer_solidarstrom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "bremer_solidarstrom.utils.jinja_methods",
#	"filters": "bremer_solidarstrom.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "bremer_solidarstrom.install.before_install"
# after_install = "bremer_solidarstrom.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bremer_solidarstrom.uninstall.before_uninstall"
# after_uninstall = "bremer_solidarstrom.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "bremer_solidarstrom.utils.before_app_install"
# after_app_install = "bremer_solidarstrom.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "bremer_solidarstrom.utils.before_app_uninstall"
# after_app_uninstall = "bremer_solidarstrom.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bremer_solidarstrom.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Project": "bremer_solidarstrom.bremer_solidarstrom.custom.project.CustomProject",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Lead": {
		"before_save": "bremer_solidarstrom.bremer_solidarstrom.custom.lead.before_save",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"bremer_solidarstrom.tasks.all"
#	],
#	"daily": [
#		"bremer_solidarstrom.tasks.daily"
#	],
#	"hourly": [
#		"bremer_solidarstrom.tasks.hourly"
#	],
#	"weekly": [
#		"bremer_solidarstrom.tasks.weekly"
#	],
#	"monthly": [
#		"bremer_solidarstrom.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "bremer_solidarstrom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "bremer_solidarstrom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "bremer_solidarstrom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["bremer_solidarstrom.utils.before_request"]
# after_request = ["bremer_solidarstrom.utils.after_request"]

# Job Events
# ----------
# before_job = ["bremer_solidarstrom.utils.before_job"]
# after_job = ["bremer_solidarstrom.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"bremer_solidarstrom.auth.validate"
# ]
