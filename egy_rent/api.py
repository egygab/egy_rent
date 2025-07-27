import frappe
from datetime import date,datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

@frappe.whitelist()
def calc_contract_items(from_date,to_date,no_months,amount,year_rate):
    contract_items=[]
    local_list={}
    ### loop to add data frappe.utils.getdate
    current_date = frappe.utils.getdate(from_date)
    from_date = frappe.utils.getdate(from_date) #datetime.strptime(from_date, "%Y-%m-%d")
    to_date = frappe.utils.getdate(to_date) #datetime.strptime(to_date, "%Y-%m-%d")
    no_months = int(no_months)
    year_rate = float(year_rate)
    amount = float(amount)
    #print(year_rate)    
    while current_date <= to_date:
        y_diff = relativedelta(current_date,from_date)
        years_between = int(y_diff.years)
        #print (str(years_between),current_date,to_date)
        #cal_amount = amount + (amount * years_between * year_rate /100)
        cal_amount = float(amount * ((1 + year_rate/100) ** (years_between )))
        local_list["collection_date"]=current_date
        local_list["amount"]=cal_amount
        current_date += relativedelta(months=no_months)

        contract_items.append(local_list)
        local_list={}
    #print(contract_items)
    return contract_items

@frappe.whitelist()
def get_contract_list(from_date,to_date,contract=None):
        contract_items=[]
        local_dec={}
        if contract :
            local_contract_item = frappe.db.sql(""" select parent,collection_date,amount,description,
									  name from `tabRental Contract list`
									where docstatus=1 and parent=%s and
									  collection_date >= %s and collection_date <= %s
									""",(contract,from_date,to_date))
             
        else:
            local_contract_item = frappe.db.sql(""" select parent,collection_date,amount,description,
									  name from `tabRental Contract list`
									where docstatus=1 and
									  collection_date >= %s and collection_date <= %s
									""",(from_date,to_date))
             
        for lcontitm in local_contract_item:
            local_dec = {} 
            local_dec ["type"] = "Installment"
            if not contract:
                local_cont = frappe.get_doc('Rental Contract', lcontitm[0],ignore_permissions=True)
                local_dec ["rental_contract"] = local_cont.name
            local_dec ["amount"] = lcontitm[2]
            local_dec ["due_date"] = lcontitm[1]
            local_dec ["description"] = lcontitm[3]
            local_dec ["type_link_name"] = lcontitm[4]
            contract_items.append(local_dec)

        return contract_items

@frappe.whitelist()
def get_maintenance_list(from_date,to_date,contract=None):
        contract_items=[]
        local_dec={}
        if contract :        
            local_contract_item = frappe.db.sql(""" select parent,collection_date,amount,description,
									  name from `tabRental Maintenance list`
									where docstatus=1 and parent=%s and
									  collection_date >= %s and collection_date <= %s
									""",(contract,from_date,to_date))
        else:
            local_contract_item = frappe.db.sql(""" select parent,collection_date,amount,description,
									  name from `tabRental Maintenance list`
									where docstatus=1 and
									  collection_date >= %s and collection_date <= %s
									""",(from_date,to_date))
        for lcontitm in local_contract_item:
            local_dec = {}
            local_dec ["type"] = "Maintenance"
            if not contract:
                local_cont = frappe.get_doc('Rental Contract', lcontitm[0],ignore_permissions=True) 
                local_dec ["rental_contract"] = local_cont.name
            local_dec ["amount"] = lcontitm[2]
            local_dec ["due_date"] = lcontitm[1]
            local_dec ["description"] = lcontitm[3]
            local_dec ["type_link_name"] = lcontitm[4]
            contract_items.append(local_dec)

        return contract_items

@frappe.whitelist()
def get_settlement_list(from_date,to_date,contract=None):
        contract_items=[]
        local_dec={}
        if contract :        
            local_item = frappe.db.sql(""" select rental_contract,settlement_date,amount,description,
									  name from `tabRental Settlement`
									where docstatus=1 and rental_contract=%s and 
									  settlement_date >= %s and settlement_date <= %s
									""",(contract,from_date,to_date))
        else:
            local_item = frappe.db.sql(""" select rental_contract,settlement_date,amount,description,
									  name from `tabRental Settlement`
									where docstatus=1 and
									  settlement_date >= %s and settlement_date <= %s
									""",(from_date,to_date))
        for lcontitm in local_item:
            local_dec = {}
			#local_cont = frappe.get_doc('Rental Contract', lcontitm[0],ignore_permissions=True) 
			#print(local_cont)
            local_dec ["type"] = "Settlement"
            if not contract:
                local_dec ["rental_contract"] = lcontitm[0]#local_cont.name
            local_dec ["amount"] = lcontitm[2]
            local_dec ["due_date"] = lcontitm[1]
            local_dec ["description"] = lcontitm[3]
            local_dec ["type_link_name"] = lcontitm[4]
            
            contract_items.append(local_dec)

        return contract_items