// Copyright (c) 2025, . and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Contract", {
	refresh(frm) {
       frm.add_custom_button(__('Get User Email Address'), function() {
           frappe.call({
                    method: 'egy_rent.egy_rent.egy_rent.doctype.rental_contract.rental_contract.calc_contract_list',
                    // Use args property to pass data to the python method
                    // Python method: def print_msg(name, age):
                    args: {name: 'some_name', age: 30},
                    callback: function(ret) {
                        // If you expect something to return form the call use the code bellow or replace it with your own code
                        if (!ret || ret.message == null) return;
                        let data = ret.message;
                        
                    }
                });
       }, __("Utilities"));
	},
});
