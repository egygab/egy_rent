# Copyright (c) 2025, . and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentalContract(Document):
	pass

@frappe.whitelist()
def calc_contract_list(doc_name):
	frappe.msgprint(doc_name)
	ren_cont = frappe.get_doc("Rental Contract", doc_name)
	#Rental Contract list
	new_item = frappe.model.add_child(ren_cont, "Rental Contract list", "items")

