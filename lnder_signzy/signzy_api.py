# Copyright (c) 2024, Aerele and contributors
# For license information, please see license.txt

import frappe
from typing import Final
import requests
from frappe import _
from frappe.utils import get_url, getdate
import re
import json
from lnder_signzy.lnder_signzy.doctype.signzy_api_request_log.signzy_api_request_log import create_log as signzy_api_log


@frappe.whitelist()
def verify_aadhaar(aadhaar_no: str):
	"""
	Verifies an Aadhaar number using the Signzy API.

	Args:
		aadhaar_no (str): The Aadhaar number to verify.
	"""
	
	def validate_aadhaar_input(pattern: str, value: str) -> bool:
		"""Validate the Aadhaar number format using a regex pattern."""
		import re
		return bool(re.match(pattern, value))

	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	# Validate the Aadhaar number format
	if not validate_aadhaar_input(pattern=r'^[2-9]{1}[0-9]{11}$', value=aadhaar_no):
		frappe.throw(title="KYC API Error", msg=_("Aadhaar Number is not valid"))

	# Prepare the API request
	url = f"{connector_doc.url}/aadhaar/verify"
	payload = json.dumps({"uid": aadhaar_no})
	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}

	# Make the API request
	response = requests.post(url, headers=headers, data=payload)
	print(response)
	# Log the API request and response
	signzy_api_log(
		api_name="Verify Aadhaar",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)

	# Handle the API response
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		error_message = response.json().get("error", {}).get("message", response.json().get("message", "Unknown error"))
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))



@frappe.whitelist()
def verify_aadhaar_ocr(front_url: str, back_url: str):
	"""
	Verifies Aadhaar card details using OCR (Optical Character Recognition).
	Args:
		front_url (str): URL of the front image of the Aadhaar card.
		back_url (str, optional): URL of the back image of the Aadhaar card. Defaults to None.
	"""

	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	url = f"{connector_doc.url}/aadhaar/extraction"
	files = [get_url() + front_url, get_url() + back_url]
	payload = json.dumps({
		"files" : files
	})
	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}
	# Make the API request
	response = requests.post(url, headers=headers, data=payload)

	# Log the API request and response
	signzy_api_log(
		api_name="Verify Aadhaar - OCR",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))


@frappe.whitelist()
def generate_otp(country_code: str , mobile_no: str):
	"""
	Generates an OTP for mobile number verification.
	Args:
		country_code (str): The country code (e.g., "91" for India).
		mobile_no (str): The mobile number to verify.
	"""

	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	url = f"{connector_doc.url}/phone/generateOtp"

	payload = json.dumps({
		"countryCode": country_code,
		"mobileNumber": mobile_no
	})

	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}

	response = requests.post(url, headers=headers, data=payload)
	print(response.text)
	# Log the API request and response
	signzy_api_log(
		api_name="Generate OTP",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
		frappe.response["generated_otp"] = True
		frappe.response["mobile_no"] = mobile_no
		frappe.response["country_code"] = country_code
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))


@frappe.whitelist()
def submit_otp(country_code: str, mobile_no: str, reference_id: str, otp: str):
	"""
	Submits the OTP for mobile number verification.

	Args:
		country_code (str): The country code (e.g., "91" for India).
		mobile_no (str): The mobile number being verified.
		reference_id (str): The reference ID received during OTP generation.
		otp (str): The OTP to submit.
	"""
	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	url = f"{connector_doc.url}/phone/getNumberDetails"

	payload = json.dumps({
		"countryCode": country_code,
		"mobileNumber": mobile_no,
		"referenceId": reference_id,
		"otp": otp,
		"extraFields": False
	})

	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}

	response = requests.post(url, headers=headers, data=payload)
	# Log the API request and response
	signzy_api_log(
		api_name="Submit OTP",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))


@frappe.whitelist()
def verify_dl(dl_number: str, dob: str, issue_date: str):
	"""
	Verifies a Driving License (DL) using the Signzy API.
	Args:
		dl_number (str): The driving license number.
		dob (str): The date of birth in 'YYYY-MM-DD' format.
		issue_date (str): The issue date of the DL in 'YYYY-MM-DD' format.
	"""
	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	dob = getdate(dob).strftime('%d/%m/%Y')
	issue_date = getdate(issue_date).strftime('%d/%m/%Y')
	url = f"{connector_doc.url}/dl_/verification"
	payload = json.dumps({
		"number": dl_number,
		"dob": dob,
		"issueDate": issue_date
	})
	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}
	response = requests.post(url, headers=headers, data=payload)
	# Log the API request and response
	signzy_api_log(
		api_name="Verify Driving License",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))

@frappe.whitelist()
def extract_dl(dl_number: str, dob: str):
	"""
	Extracts details from a Driving License (DL) using the Signzy API.
	Args:
		dl_number (str): The driving license number.
		dob (str): The date of birth in 'YYYY-MM-DD' format.
	"""
	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	dob = getdate(dob).strftime('%d/%m/%Y')
	url = f"{connector_doc.url}/dl_number/based_search"

	payload = json.dumps({
		"number": dl_number,
		"dob": dob
	})

	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}

	response = requests.post(url, headers=headers, data=payload)
	# Log the API request and response
	signzy_api_log(
		api_name="Verify Driving License Details",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))


@frappe.whitelist()
def verify_pan(pan: str, name: str, dob: str):
	"""
	Verifies a PAN (Permanent Account Number) using the Signzy API.

	Args:
		pan (str): The PAN number.
		name (str): The name associated with the PAN.
		dob (str): The date of birth in 'YYYY-MM-DD' format.
	"""
	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	dob = getdate(dob).strftime('%d/%m/%Y')
	url = f"{connector_doc.url}/pan/verify"

	payload = json.dumps({
		"pan": pan,
		"name": name,
		"dob": dob
	})

	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}

	response = requests.post(url, headers=headers, data=payload)
	# Log the API request and response
	signzy_api_log(
		api_name="Verify PAN",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))


@frappe.whitelist()
def verify_upi(vpa:str, name:str):
	print("ddddddddddddddddddddddd")
	"""
	Verifies a UPI (Unified Payments Interface) ID using the Signzy API.

	Args:
		vpa (str): The Virtual Payment Address (VPA) to verify.
		name (str): The name to match with the VPA.
	"""
	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	fuzzy = False
	url = f"{connector_doc.url}/bankAccountVerification/upiVerifications"
	payload = json.dumps({
		"vpa" : vpa,
		"name" : name,
		"fuzzy" : fuzzy
	})

	headers = {
	'Authorization': connector_doc.get_password("authorization"),
	'Content-Type': 'application/json'
	}

	response = requests.post(url, headers=headers, data=payload)
	# Log the API request and response
	signzy_api_log(
		api_name="Verify UPI",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))


@frappe.whitelist()
def verify_bank_acc(acc_no: str, ifsc_code: str, mobile_no: str, name: str ,email: str = None):
	"""
	Verifies a bank account using the Signzy API.

	Args:
		acc_no (str): The bank account number.
		ifsc_code (str): The IFSC code of the bank.
		mobile_no (str): The mobile number associated with the bank account.
		name (str): The name associated with the bank account.
		email (str, optional): The email address associated with the bank account. Defaults to None.
	"""

	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	url = f"{connector_doc.url}/bankaccountverifications/advancedverification"

	payload = {
		"beneficiaryAccount": acc_no,
		"beneficiaryIFSC": ifsc_code,
		"beneficiaryMobile": mobile_no,
		"beneficiaryName": name
	}

	if email:
		payload["email"] = email
	payload = json.dumps(payload)

	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}

	response = requests.post(url, headers=headers, data=payload)
	# Log the API request and response
	signzy_api_log(
		api_name="Verify Bank Account",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))


@frappe.whitelist()
def verify_rc(vehicle_no: str):
	# Fetch the Signzy Connector details
	connector_doc = frappe.get_single("Signzy Connector")
	
	# Check if the connector configuration is valid
	if not (connector_doc.url and connector_doc.authorization):
		frappe.throw(title="Configuration Error", msg=_("Signzy Connector URL or Authorization is not set"))

	url = f"{connector_doc.url}/vehicle/detailedsearches"

	payload = json.dumps({
		"vehicleNumber": vehicle_no,
		"blacklistCheck": "true",
		"splitAddress": "true"
	})

	headers = {
		'Authorization': connector_doc.get_password("authorization"),
		'Content-Type': 'application/json'
	}

	response = requests.post(url, headers=headers, data=payload)
	# Log the API request and response
	signzy_api_log(
		api_name="Verify Vehicle RC",
		api_endpoint=url,
		api_request_header=headers,
		api_request_data=payload,
		api_response=response.text,
		api_response_status_code=response.status_code
	)
	if response.ok:
		frappe.response["message"] = response.json()
	else:
		if ("error" in response.json()):
			error_message = response.json().get("error").get("message")
		else:
			error_message = response.json().get("message")
		frappe.throw(title="Signzy API Error", msg=_(f"{error_message}"))
