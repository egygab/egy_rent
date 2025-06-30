// Copyright (c) 2025, . and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Batch", {
	refresh(frm) {
        
        frm.get_field("batch_items").grid.cannot_add_rows = true;
        refresh_field("batch_items");

	},
});
