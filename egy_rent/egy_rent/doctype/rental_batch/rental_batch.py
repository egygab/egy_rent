# Copyright (c) 2025, . and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class RentalBatch(Document):
	def after_insert(self):
		local_contract_item = frappe.db.sql(""" select collection_date
									
									""",(self.rental_unit,self.from_date,self.to_date))
		
