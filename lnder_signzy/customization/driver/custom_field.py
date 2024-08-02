from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def driver_field_customization():
	create_driver_custom_field()
	driver_property_setter()

def create_driver_custom_field():
	custom_fields = {
		"Driver": [
			dict(
				fieldname="custom_verify_driving_license",
				label="Verify Driving license",
				fieldtype="Button",
				insert_after="license_number",
			), 
			dict(
				fieldname="custom_driving_license_verified",
				label="Is Driving license Verified",
				fieldtype="Check",
				insert_after="custom_verify_driving_license",
				read_only=1
			)
		]
	}
	create_custom_fields(custom_fields, update=True)

def driver_property_setter():
	pass