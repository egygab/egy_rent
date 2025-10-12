// Copyright (c) 2025, . and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Contract", {
	refresh(frm) {
       frm.add_custom_button(__('Update List'), function() {
        if (frm.doc.docstatus === 1) { // docstatus 1 means Submitted
            // Remove the custom button
            frappe.msgprint("Document should not submit") ;
        }  else  {
        frappe.call({
            method: 'egy_rent.api.calc_contract_items',
            args: {from_date: frm.doc.effective_date, to_date: frm.doc.end_date,
                no_months:frm.doc.contract_periods_in_months, 
                amount: frm.doc.amount, year_rate: frm.doc.annual_increase,
            },
            }).done((r) => { 
                    frm.doc.table_rental_list = [] 
                    $.each(r.message, function(_i, e){
                        let entry = frm.add_child("table_rental_list");
                        entry.collection_date = e.collection_date;
                        entry.description = "Installment for unit " + frm.doc.contract_name + " On " + moment(e.collection_date).format("DD-MM-YYYY") ;
                        entry.amount=e.amount;
                        })
                    refresh_field("table_rental_list") 
                })

        frm.doc.rental_maintenance_list = [] 
        if (frm.doc.maintenance_effective_date && frm.doc.maintenance_end_date) {
            //alert(frm.doc.maintenance_effective_date);
        
        frappe.call({
            method: 'egy_rent.api.calc_contract_items',
            args: {from_date: frm.doc.maintenance_effective_date, to_date: frm.doc.maintenance_end_date,
                no_months:frm.doc.maintenance_periods_in_months, 
                amount: frm.doc.maintenance_amount, year_rate: frm.doc.maintenance_annual_increase,
            },
            }).done((r) => { 
                    frm.doc.rental_maintenance_list = [] 
                    $.each(r.message, function(_i, e){
                        let entry = frm.add_child("rental_maintenance_list");
                        entry.collection_date = e.collection_date;
                        entry.description = "Maintenance for unit " + frm.doc.contract_name + " On " + moment(e.collection_date).format("DD-MM-YYYY") ;
                        entry.amount=e.amount;
                        })
                    refresh_field("rental_maintenance_list") 
                })
        }
        refresh_field("rental_maintenance_list") 
                
        //    frappe.call({
        //             method: 'egy_rent.egy_rent.doctype.rental_contract.rental_contract.calc_contract_list',
        //             // Use args property to pass data to the python method
        //             // Python method: def print_msg(name, age):
        //             args: {doc_name: frm.doc.name, age: 30},
        //             callback: function(ret) {
        //                 // If you expect something to return form the call use the code bellow or replace it with your own code
        //                 if (!ret || ret.message == null) return;
        //                 let data = ret.message;
                        
        //             }
        //         });
    }// end if
       }, __("Utilities"));

/////////////////////////////
    // frm.add_custom_button(__('Create Cheque Wallet'), function() {
    //     let d = new frappe.ui.Dialog({
    //         title: __('Confirmation'),
    //         fields: [
    //             {
    //                 fieldname: 'add_maince_list',
    //                 label: __('Add Maintenance List'),
    //                 fieldtype: 'Check'
    //             },
    //             {
    //                 fieldname: 'start_check_number',
    //                 label: __('Start Check Number'),
    //                 fieldtype: 'Int'
    //             }                
    //         ],
    //         primary_action_label: __('Submit'),
    //         primary_action: function(values) {
    //             if (values.add_maince_list) {
    //                 frappe.msgprint(__('Thank you for agreeing!' ));
    //                 console.log(frm.doc.name);
    //                 console.log(values.start_check_number);
    //                 d.hide();
    //             } else {
    //                 frappe.msgprint(__('Please agree to the terms to proceed.'));
    //             }
    //         }
    //     });
    //     d.show();


    //        }, __("Utilities"));


	},
});


cur_frm.fields_dict.default_bank.get_query = function(doc) {
	return {
		filters: [
			["Account", "account_type", "=", "Bank"],
			["Account", "root_type", "=", "Asset"],
			["Account", "is_group", "=",0],
			["Account", "company", "=", doc.company]
		]
	}
}