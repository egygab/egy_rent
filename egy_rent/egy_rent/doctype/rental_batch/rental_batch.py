# Copyright (c) 2025, . and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from egy_rent import api

class RentalBatch(Document):
	#def after_insert(self):
	def after_insert(self):

		local_dec = api.get_contract_list(self.from_date,self.to_date)
		for lcontitm in local_dec:
			self.append('batch_items', lcontitm)
		self.save()

		local_dec = api.get_maintenance_list(self.from_date,self.to_date)
		for lcontitm in local_dec:
			self.append('batch_items', lcontitm)
		self.save()

		local_dec = api.get_settlement_list(self.from_date,self.to_date)
		for lcontitm in local_dec:
			self.append('batch_items', lcontitm)
		self.save()	


	def on_submit(self):
		local_items = frappe.db.sql(""" SELECT DISTINCT rental_contract
									   from `tabRental Batch Items`
									where parent = %s
									""",(self.name))
		for lcontitm in local_items:
			child = frappe.new_doc("Rental Collection Request")
			child.rental_contract = lcontitm[0]
			child.request_date = self.batch_date
			child.from_date = self.from_date
			child.to_date = self.to_date
			child.request_title = "Request from " + str(self.name)
			child.rental_batch = self.name
			child.insert(ignore_permissions=True)
			child.submit()

		frappe.db.commit()




		
		# cust_name = "Grant Plastics Ltd."
		# local_custmr = frappe.get_doc('Customer', cust_name ,ignore_permissions=True) 
		# child = frappe.new_doc("Sales Invoice")
		# child.customer =  local_custmr
		# child.posting_date = frappe.utils.nowdate()
		# child.due_date = frappe.utils.nowdate()
		# child.title ="test---"
		# #child.is_pos = 1

		# local_item = {}
		# ########
		# #local_item ["item_code"] ="SKU005"
		# local_item ["qty"] = 1
		# local_item ["item_name"] = "test"
		# local_item ["uom"] = "Unit"
		# local_item ["rate"] = 120
		# local_item ["amount"] = 120
		# local_item ["income_account"] = "4110 - Sales - ED"
		# local_item ["description"] = "test description"
		
		# child.append = ('items', local_item)
		# #######
		
		# payments = {
		# 	'mode_of_payment': "Cash",
		# 	'amount': 120,
		# 	'type': "Cash",
		# 	'default': 1
		# }	

		# print ("child",child)
		# #child.append("payments", payments)
		# #child.set_missing_values()
		

		# child.insert(ignore_permissions=True)
		# frappe.db.commit()