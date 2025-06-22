import frappe
@frappe.whitelist()
def calc_contract_items(from_date,to_date,months,amount,year_rate):
    contract_items=[]
    local_list={}
    ### loop to add data
    local_list["collection_date"]=from_date
    local_list["amount"]=amount

    contract_items.append(local_list)
    return contract_items