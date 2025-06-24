// Copyright (c) 2025, . and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Rental Integration Import Tool", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Rental Integration Import Tool", "btn_import", function(frm) { 

    //frappe.msgprint(frm.doc.business_date)
       frappe.call({
                method: 'egy_rent.tasks.pull_integration_invoices',
                args: {business_date: frm.doc.business_date},
                callback: function(ret) {
                    // If you expect something to return form the call use the code bellow or replace it with your own code
                    if (!ret || ret.message == null) return;
                    let data = ret.message;
                    
                }
            }); 
        frappe.msgprint("We stared importing the data!")
});