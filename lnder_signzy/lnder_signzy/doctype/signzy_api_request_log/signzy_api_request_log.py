# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt


import json
import frappe
from frappe.model.document import Document


class SignzyAPIRequestLog(Document):
	pass

def create_log(api_name, api_endpoint, api_request_header=None, api_request_data=None, api_response=None, api_response_status_code=None):
	log_doc = frappe.new_doc("Signzy API Request Log")
	log_doc.api_method = api_name
	log_doc.url = api_endpoint

	if api_request_header:
		if isinstance(api_request_header, str):
			try:
				api_request_header = json.loads(api_request_header)
			except json.JSONDecodeError:
				log_doc.header = api_request_header
		if isinstance(api_request_header, dict):
			log_doc.header = json.dumps(api_request_header, indent=4)

	if api_request_data:
		if isinstance(api_request_data, str):
			try:
				api_request_data = json.loads(api_request_data)
			except json.JSONDecodeError:
				log_doc.payload = api_request_data
		if isinstance(api_request_data, dict):
			log_doc.payload = json.dumps(api_request_data, indent=4)

	if api_response:
		if isinstance(api_response, str):
			try:
				log_doc.response = json.dumps(json.loads(api_response), indent=4)
			except json.JSONDecodeError:
				log_doc.response = api_response
		elif isinstance(api_response, dict):
			log_doc.response = json.dumps(api_response, indent=4)
		elif not isinstance(api_response, (str, dict)):
			try:
				log_doc.response = json.dumps(api_response.json(), indent=4)
			except (TypeError, ValueError):
				log_doc.response = str(api_response)
	log_doc.status_code = api_response_status_code
	log_doc.insert(ignore_permissions=True)
	frappe.db.commit()
 
def delete_older_logs():
	frappe.db.sql(
			""" DELETE FROM `tabSignzy API Request Log`
			WHERE `creation` < (NOW() - INTERVAL '1000' DAY)
		"""
		)