frappe.ui.form.on("Employee", {
	refresh: function (frm) {
		//
	},
	custom_verify_mobile: function (frm) {
		if (!frm.doc.custom_mobile_number) {
			return;
		}
		frappe.call({
			method: "lnder_signzy.signzy_api.generate_otp",
			args: {
				country_code: "91",
				mobile_no: frm.doc.custom_mobile_number
			},
			freeze: true,
			freeze_message: __("Verifying...."),
			callback: function (r) {
				if (!r.exec && r.message.result && r.generated_otp) {
					frappe.show_alert({
						message: __('OTP sent successfully'),
						indicator: 'green'
					}, 5);
	
					var reference_id = r.message.result.referenceId;
					var mobile_no = frm.doc.custom_mobile_number;
					var country_code = "91";
	
					if (reference_id) {
						frappe.prompt([
							{
								label: __("OTP"),
								fieldname: 'otp',
								fieldtype: 'Data'
							}
						],
						function (data) {
							submit_otp(frm, country_code, mobile_no, reference_id, data.otp);
						},
						__("Enter OTP for Verification"));
					}
				}
			}
		});
	},
	custom_verify_aadhar: (frm) => {
		if (frm.doc.custom_verify_aadhar || !frm.doc.custom_aadhar_number) {
			return;
		}
	
		frappe.call({
			method: "lnder_signzy.signzy_api.verify_aadhaar",
			args: {
				aadhaar_no: frm.doc.custom_aadhar_number
			},
			freeze: true,
			freeze_message: __("Verifying Aadhaar Number"),
			callback: (r) => {
				if (!r.exec && r.message.result) {
					handle_aadhaar_verification_result(frm, r.message.result);
				}
			}
		});
	},
	custom_verify_aadhar_ocr: (frm) => {
		if (frm.doc.custom_verify_aadhar_ocr || !frm.doc.custom_aadhar_card_front_image || !frm.doc.custom_aadhar_card_back_image) {
			return;
		}
	
		const args = {
			front_url: frm.doc.custom_aadhar_card_front_image,
			back_url: frm.doc.custom_aadhar_card_back_image
		};
	
		frappe.call({
			method: "lnder_signzy.signzy_api.verify_aadhaar_ocr",
			args: args,
			freeze: true,
			freeze_message: __("Verifying Aadhaar OCR"),
			callback: (r) => {
				if (!r.exec && r.message.result) {
					handle_aadhaar_ocr_verification_result(frm, r.message.result);
				}
			}
		});
	},
	custom_verify_pan: (frm) => {
		if (!frm.doc.first_name) {
			frappe.throw(__("Enter the Name"));
		}
	
		if (!frm.doc.date_of_birth) {
			frappe.throw(__("Enter the Date of Birth"));
		}
	
		const args = {
			pan: frm.doc.custom_pan,
			name: frm.doc.employee_name,
			dob: frm.doc.date_of_birth
		};
	
		frappe.call({
			method: "lnder_signzy.signzy_api.verify_pan",
			args: args,
			freeze: true,
			freeze_message: __("Verifying PAN Number"),
			callback: (r) => {
				if (!r.exec && r.message.result) {
					handle_pan_verification_result(frm, r.message.result);
				}
			}
		});
	}	
});
function submit_otp(frm, country_code, mobile_no, reference_id, otp) {
	frappe.call({
		method: "lnder_signzy.signzy_api.submit_otp",
		args: {
			country_code: country_code,
			mobile_no: mobile_no,
			reference_id: reference_id,
			otp: otp
		},
		freeze: true,
		freeze_message: __("Verifying OTP"),
		callback: function (r) {
			if (!r.exec) {
				if (r.message.result) {
					frm.set_value("custom_is_mobile_no_verified", 1);
					frappe.msgprint(__("Mobile Number Verified Successfully"));
				} else {
					frappe.msgprint(__("OTP Verification Failed"));
				}
			}
		}
	});
}

function handle_aadhaar_verification_result(frm, result) {
	if (result.verified === "true") {
		frm.set_value("custom_is_aadhar_verified", 1)
		frappe.msgprint(__("Aadhaar Number Verification Successfull"));
	} else {
		frappe.msgprint(__("Aadhaar Number Verification Failed"));
	}
}

function handle_aadhaar_ocr_verification_result(frm, result) {
	frm.set_value("custom_is_aadhar_ocr_verified", 1)
	frappe.msgprint(__("Aadhaar Number Verified Successfully"));
}

function handle_pan_verification_result(frm, result) {
	const isVerified = result.panStatus === "E" && result.dob === "Y" && result.name === "Y";
	const verificationStatus = isVerified ? 1 : 0;
	const message = isVerified ? __("PAN Number Verified Successfully") : __("PAN Verification Failed");

	frm.set_value("custom_is_pan_verified", verificationStatus)
	frappe.msgprint(message);
}