from lnder_signzy.customization.employee.custom_field import employee_field_customization
from lnder_signzy.customization.driver.custom_field import driver_field_customization

def after_migrate():
	employee_field_customization()
	driver_field_customization()