# Copyright (c) 2025, . and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from egy_rent import api

class RentalChequeWallet(Document):
	def after_insert(self):

		local_cont = frappe.get_doc('Rental Contract', self.rental_contract,ignore_permissions=True)
		try:
			cheq_number = int(self.start_check_number)
		except:
			cheq_number=1

		for lcontitm in local_cont.table_rental_list:
			local_dec = {}
			local_dec ["cheque_no"] = cheq_number
			local_dec ["bank"] = self.bank
			local_dec ["amount"] = lcontitm.amount
			local_dec ["contract_item_type"] = "Rental Contract list"
			local_dec ["contract_item_name"] = lcontitm.name
			local_dec ["cheque_date"] = lcontitm.collection_date
			local_dec ["bank_location"] = self.bank_location
			local_dec ["description"] = lcontitm.description
			cheq_number=cheq_number+1
			self.append('rental_cheque_wallet_list', local_dec)

		for lcontitm in local_cont.rental_maintenance_list:
			local_dec = {}
			local_dec ["cheque_no"] = cheq_number
			local_dec ["bank"] = self.bank
			local_dec ["amount"] = lcontitm.amount
			local_dec ["contract_item_type"] = "Rental Maintenance Item"
			local_dec ["contract_item_name"] = lcontitm.name
			local_dec ["cheque_date"] = lcontitm.collection_date
			local_dec ["bank_location"] = self.bank_location
			local_dec ["description"] = lcontitm.description
			cheq_number=cheq_number+1
			self.append('rental_cheque_wallet_list', local_dec)
		self.save()

		# local_dec = api.get_maintenance_list(self.from_date,self.to_date,self.rental_contract)
		# for lcontitm in local_dec:
		# 	self.append('collection_request_items', lcontitm)
		# self.save()

	def before_submit(self):
		### Get customer data
		contract_ = frappe.get_doc('Rental Contract', self.rental_contract)
		for lcontitm in self.rental_cheque_wallet_list:
			new_chq = frappe.new_doc("Cheque Master")
			new_chq.cheque_no = lcontitm.cheque_no
			new_chq.cheque_date = lcontitm.cheque_date
			new_chq.amount = lcontitm.amount
			new_chq.bank = lcontitm.bank
			new_chq.company = lcontitm.company
			new_chq.cheque_type = "Receivable"
			new_chq.party_type = "Customer"
			print ("===============================")
			print(contract_)
			print (contract_.link_customer)
			new_chq.party_name = contract_.link_customer
			new_chq.bank_location = lcontitm.bank_location
			new_chq.remarks = lcontitm.description
			new_chq.rental_cheque_wallet = self.name
			new_chq.current_cheque_status = "Draft"
			new_chq.insert()

		frappe.db.commit()
