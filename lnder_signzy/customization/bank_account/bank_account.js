frappe.ui.form.on("Bank Account", {
	custom_verify_upi_id: (frm) => {
		if (!frm.doc.account_name) {
			frappe.throw(__("Enter account holder name"));
		}
		if (!frm.doc.custom_upi_id) {
			frappe.throw(__("Enter UPI ID"));
		}
		const args = {
			vpa: frm.doc.custom_upi_id,
			name: frm.doc.account_name
		};

		frappe.call({
			method: "lnder_signzy.signzy_api.verify_upi",
			args: args,
			freeze: true,
			freeze_message: __("Verifying UPI ID"),
			callback: (r) => {
				if (!r.exec && r.message.result) {
					handle_upi_verification_result(frm, r.message.result);
				}
			}
		});
	},
	custom_verify_bank_account: (frm) => {
		// if (!frm.doc.custom_verified_mobile || !frm.doc.custom_verified_pan) {
		// 	frappe.throw(__("Please verify Mobile and PAN before verifying Bank Account"));
		// }
	
		const args = {
			acc_no: frm.doc.bank_account_no,
			name: frm.doc.account_name,
			ifsc_code: frm.doc.branch_code,
			mobile_no: frm.doc.custom_mobile_no,
			// email: frm.doc.personal_email || undefined
		};
	
		frappe.call({
			method: "lnder_signzy.signzy_api.verify_bank_acc",
			args: args,
			freeze: true,
			freeze_message: __("Verifying Bank Account..."),
			callback: (r) => {
				if (!r.exec && r.message.result) {
					handle_bank_account_verification_result(frm, r.message.result);
				}
			}
		});
	}
});
function handle_upi_verification_result(frm, result) {
	if (result.verified === "true") {
		frm.set_value("custom_is_upi_verified", 1)
		frappe.msgprint(__("UPI ID Verified Successfully"));
	} else {
		frm.set_value("custom_is_upi_verified", null)
	}
}

function handle_bank_account_verification_result(frm, result) {
	const isVerified = result.active === "yes" && result.reason === "success";
	const verificationStatus = isVerified ? 1 : 0;
	const message = isVerified ? __("Bank Account Verified Successfully") : __("Bank Account Verification Failed");

	frm.set_value("is_bank_account_verified", verificationStatus)
	frappe.msgprint(message);
}