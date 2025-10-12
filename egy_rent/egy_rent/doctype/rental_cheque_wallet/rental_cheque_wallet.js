// Copyright (c) 2025, . and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Rental Cheque Wallet", {
// 	refresh(frm) {

// 	},
// });


cur_frm.fields_dict["rental_cheque_wallet_list"].grid.get_field("bank").get_query = function (doc, cdt, cdn)  {
    var row = locals[cdt][cdn];
	return {
		filters: [ 
			["Account", "account_type", "=", "Bank"],
			["Account", "root_type", "=", "Asset"],
			["Account", "is_group", "=",0],
			["Account", "company", "=", row.company]
		]
	}
}


cur_frm.fields_dict.bank.get_query = function(doc) {
	return {
		filters: [
			["Account", "account_type", "=", "Bank"],
			["Account", "root_type", "=", "Asset"],
			["Account", "is_group", "=",0],
			["Account", "company", "=", doc.company]
		]
	}
}