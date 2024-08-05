frappe.ui.form.on("Driver", {
	custom_verify_driving_license: function(frm) {
		if (frm.doc.license_number) {
			frm.trigger("custom_verify_driving_license");
		}
	},
	custom_verify_driving_license: (frm) => {
		console.log("Verifying Driving License...");
		if (!frm.doc.custom_date_of_birth) {
			frappe.throw(__("Enter Date of Birth"));
		}
	
		const args = {
			dl_number: frm.doc.license_number,
			dob: frm.doc.custom_date_of_birth,
			issue_date: frm.doc.issuing_date
		};
	
		frappe.call({
			method: "lnder_signzy.signzy_api.verify_dl",
			args: args,
			freeze: true,
			freeze_message: __("Verifying Driving License..."),
			callback: (r) => {
				if (!r.exec && r.message.result) {
					handle_dl_verification_result(frm, r.message.result);
				}
			}
		});
	}
});
function handle_dl_verification_result(frm, result) {
	if (result.verified) {
		if (result.moreInfo && result.moreInfo.expiryDate) {
			const expiry_date_obj = new Date(result.moreInfo.expiryDate);
			frm.set_value("expiry_date", expiry_date_obj);
		}
		frm.set_value("custom_driving_license_verified", 1);
		frm.refresh_fields();
		frappe.msgprint(__(result.message));
	} else {
		frm.refresh_fields();
		frappe.msgprint(__(result.message));
	}
}