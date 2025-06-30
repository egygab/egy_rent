import frappe
from datetime import date,datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

@frappe.whitelist()
def calc_contract_items(from_date,to_date,no_months,amount,year_rate):
    contract_items=[]
    local_list={}
    ### loop to add data
    current_date = datetime.strptime(from_date, "%Y-%m-%d")
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")
    no_months = int(no_months)
    year_rate = float(year_rate)
    amount = float(amount)
    #print(year_rate)    
    while current_date <= to_date:
        y_diff = relativedelta(current_date,from_date)
        years_between = int(y_diff.years)
        cal_amount = amount + (amount * years_between * year_rate /100) 
        local_list["collection_date"]=current_date
        local_list["amount"]=cal_amount
        current_date += relativedelta(months=no_months)

        contract_items.append(local_list)
        local_list={}
    #print(contract_items)
    return contract_items

