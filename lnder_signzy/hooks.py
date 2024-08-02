app_name = "lnder_signzy"
app_title = "Lnder Signzy"
app_publisher = "Aerele"
app_description = "Signzy API"
app_email = "hello@aerele.in"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lnder_signzy/css/lnder_signzy.css"
# app_include_js = "/assets/lnder_signzy/js/lnder_signzy.js"

# include js, css files in header of web template
# web_include_css = "/assets/lnder_signzy/css/lnder_signzy.css"
# web_include_js = "/assets/lnder_signzy/js/lnder_signzy.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lnder_signzy/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
    "Employee" : "customization/employee/employee.js",
    "Driver" : "customization/driver/driver.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "lnder_signzy/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "lnder_signzy.utils.jinja_methods",
# 	"filters": "lnder_signzy.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "lnder_signzy.install.before_install"
# after_install = "lnder_signzy.install.after_install"
after_migrate = "lnder_signzy.after_migrate.after_migrate"
# Uninstallation
# ------------

# before_uninstall = "lnder_signzy.uninstall.before_uninstall"
# after_uninstall = "lnder_signzy.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lnder_signzy.utils.before_app_install"
# after_app_install = "lnder_signzy.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lnder_signzy.utils.before_app_uninstall"
# after_app_uninstall = "lnder_signzy.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lnder_signzy.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lnder_signzy.tasks.all"
# 	],
# 	"daily": [
# 		"lnder_signzy.tasks.daily"
# 	],
# 	"hourly": [
# 		"lnder_signzy.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lnder_signzy.tasks.weekly"
# 	],
# 	"monthly": [
# 		"lnder_signzy.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "lnder_signzy.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lnder_signzy.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lnder_signzy.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lnder_signzy.utils.before_request"]
# after_request = ["lnder_signzy.utils.after_request"]

# Job Events
# ----------
# before_job = ["lnder_signzy.utils.before_job"]
# after_job = ["lnder_signzy.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lnder_signzy.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

