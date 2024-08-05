from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def employee_field_customization():
	create_employee_custom_field()

def create_employee_custom_field():
	custom_fields = {
		"Employee": [
			dict(
				fieldname="custom_verify_mobile",
				label="Verify Mobile",
				fieldtype="Button",
				depends_on = "eval: doc.custom_mobile_number",
				insert_after="custom_mobile_number",
			),
			dict(
				fieldname="custom_is_mobile_no_verified",
				label="Is Mobile Verified",
				fieldtype="Check",
				read_only = True,
				insert_after="custom_verify_mobile",
			),
			dict(
				fieldname="custom_verify_aadhar",
				label="Verify Aadhar",
				fieldtype="Button",
				depends_on = "eval: doc.custom_aadhar_number",
				insert_after="custom_aadhar_number",
			),
			dict(
				fieldname="custom_is_aadhar_verified",
				label="Is Aadhar Verified",
				fieldtype="Check",
				read_only = True,
				insert_after="custom_verify_aadhar",
			),
			dict(
				fieldname="custom_verify_aadhar_ocr",
				label="Verify Aadhaar OCR",
				fieldtype="Button",
				depends_on = "eval: doc.custom_aadhar_card_front_image",
				insert_after="custom_aadhar_card_back_image",
			),
			dict(
				fieldname="custom_is_aadhar_ocr_verified",
				label="Is Aadhar OCR Verified",
				fieldtype="Check",
				read_only = True,
				insert_after="custom_verify_aadhar_ocr",
			),
			dict(
				fieldname="custom_verify_pan",
				label="Verify PAN",
				fieldtype="Button",
				depends_on = "eval:doc.custom_pan",
				insert_after="custom_pan",
			),
			dict(
				fieldname="custom_is_pan_verified",
				label="Is PAN Verified",
				fieldtype="Check",
				read_only = True,
				insert_after="custom_verify_pan",
			),
		]
	}
	create_custom_fields(custom_fields, update=True)