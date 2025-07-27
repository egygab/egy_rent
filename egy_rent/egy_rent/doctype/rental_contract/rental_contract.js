// Copyright (c) 2025, . and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Contract", {
	refresh(frm) {
       frm.add_custom_button(__('Update List'), function() {
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
       }, __("Utilities"));
	},
});
