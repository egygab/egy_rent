# Copyright (c) 2025, . and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from egy_rent import api

class RentalCollectionRequest(Document):
	def after_insert(self):

		local_dec = api.get_contract_list(self.from_date,self.to_date,self.rental_contract)
		for lcontitm in local_dec:
			self.append('collection_request_items', lcontitm)
		self.save()

		local_dec = api.get_maintenance_list(self.from_date,self.to_date,self.rental_contract)
		for lcontitm in local_dec:
			self.append('collection_request_items', lcontitm)
		self.save()

		local_dec = api.get_settlement_list(self.from_date,self.to_date,self.rental_contract)
		for lcontitm in local_dec:
			self.append('collection_request_items', lcontitm)
		self.save()

	def on_submit(self):
		local_cont = frappe.get_doc('Rental Contract', self.rental_contract,ignore_permissions=True)

		for child_doc in self.collection_request_items:
			child_invoice = frappe.new_doc("Sales Invoice")
			child_invoice.customer=self.link_customer
			##############
			if child_doc.type == "Installment" :
				service_code = local_cont.contract_service #"SRV01"
				taxes_code = local_cont.contract_sales_taxes_template # "Egypt Tax - ED"
			if child_doc.type == "Maintenance" :
				service_code = local_cont.maintenance_service #"SRV01"
				taxes_code = local_cont.maintenance_sales_taxes_template # "Egypt Tax - ED"
			if child_doc.type == "Settlement" : ### TODO change the Settlement data
				local_stlm = frappe.get_doc('Rental Settlement', child_doc.type_link_name,ignore_permissions=True)
				service_code = local_stlm.service_item #"SRV01"
				taxes_code = local_stlm.sales_taxes_template # "Egypt Tax - ED"

			if child_doc.amount < 0 :
				invoice_amount = abs(child_doc.amount)
				invoice_qty = -1
				child_invoice.is_return = True
			else:
				invoice_amount = child_doc.amount
				invoice_qty = 1

			child_invoice.append("items", {"item_code": service_code,"item_name": child_doc.description, "qty": invoice_qty , "rate": invoice_amount})
			child_invoice.remarks=child_doc.description
			if taxes_code:
				child_invoice.taxes_and_charges = taxes_code #"Egypt Tax - ED"
			sinvoice=child_invoice.insert(ignore_permissions=True)
			child_doc.sales_invoice=sinvoice
			child_doc.save()

		# child = frappe.new_doc("Sales Invoice")
		# child.customer=self.link_customer
		# child.append("items", {"item_code": "SRV01", "qty": 1, "rate": 50})
		# #child.taxes_and_charges = "Egypt Tax - ED"
		# #sinvoice=child.save(ignore_permissions=True)
		# sinvoice=child.insert(ignore_permissions=True)
		# self.sales_invoice=sinvoice
		# self.save()
		# #child.submit()