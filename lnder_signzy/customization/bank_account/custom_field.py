from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def bank_account_field_customization():
	create_bank_account_custom_field()
	bank_account_property_setter()

def create_bank_account_custom_field():
	custom_fields = {
		"Bank Account": [
            dict(
				fieldname="custom_verify_bank_account",
				label="Verify Bank Account",
				fieldtype="Button",
				insert_after="bank_account_no",
				depends_on="eval:doc.bank_account_no"
			), 
			dict(
				fieldname="is_bank_account_verified",
				label="Is Bank Account Verified",
				fieldtype="Check",
				insert_after="custom_verify_bank_account",
				read_only=1
			),
			dict(
				fieldname="custom_verify_upi_id",
				label="Verify UPI ID",
				fieldtype="Button",
				insert_after="custom_upi_id",
				depends_on="eval:doc.custom_upi_id"
			), 
			dict(
				fieldname="custom_is_upi_verified",
				label="Is UPI Verified",
				fieldtype="Check",
				insert_after="custom_verify_upi_id",
				read_only=1
			)
		]
	}
	create_custom_fields(custom_fields, update=True)

def bank_account_property_setter():
	pass