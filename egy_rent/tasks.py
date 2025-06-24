import frappe
import requests
import json
import time
from datetime import date, timedelta

def foodics_response(endpoint,data={},headers={}):
    response = requests.request("GET", endpoint, headers=headers, data=data)
    return response

def save_foodics_invoices(response,store_name,data={},headers={}):
    store_date = response.json().get('data')
    print (store_date)
    for date_item in store_date:
        #print (date_item['id'])
        new_si = frappe.new_doc("Rental Integration Sales")
        new_si.store = store_name
        new_si.external_id = date_item['id']
        new_si.invoice_date = date_item['business_date']
        new_si.invoice_amount = date_item['total_price']
        new_si.net_amount = date_item['subtotal_price']
        new_si.external_reference = date_item['reference']
        new_si.external_type = date_item['type']
        if date_item['type'] == 1 :
            new_si.external_type_name="Pending"
        elif date_item['type'] == 2 :
            new_si.external_type_name="Active"
        elif date_item['type'] == 3 :
            new_si.external_type_name="Declined"
        elif date_item['type'] == 4 :
            new_si.external_type_name="Closed"
        elif date_item['type'] == 5 :
            new_si.external_type_name="Returned"
            new_si.invoice_amount = float(date_item['total_price']) * -1
            new_si.net_amount = float(date_item['subtotal_price'])* -1   
        elif date_item['type'] == 6 :
            new_si.external_type_name="Joined"
        elif date_item['type'] == 7 :
            new_si.external_type_name="Void"            
        elif date_item['type'] == 8 :
            new_si.external_type_name="Draft"


        ### get order data
        # endpoint="https://api.foodics.com/v5/orders/" + str(date_item['id'])
        # print(data)
        # order_response = foodics_response(endpoint, headers=headers, data=data)
        # print (order_response.json())
        # time.sleep(2)  # Pause for 2 seconds
        #############
        #new_si.insert()
        try:
            new_si.insert()
        except:
            pass
    frappe.db.commit()
##bench --site site1.local execute egy_rent.tasks.pull_integration_invoices
##bench --site system.egygab.com execute egy_rent.tasks.pull_integration_invoices
@frappe.whitelist()
def pull_integration_invoices(business_date = date.today() - timedelta(days=1)):
    stores = frappe.db.get_all('Rental Integration Master')
    for store in stores:
        store_ = frappe.get_doc('Rental Integration Master', store.name)
        #print (store_.token)
        if store_.integration_type == "foodics" :
            ################### foodics ##########################
            url = "https://api.foodics.com/v5/orders?filter[business_date]=" + str(business_date) + "&filter[branch_id]=" + str(store_.branch_id)
            payload = {'charge_id': '9775780c-f713-453c-bf12-6c9245134c05'}
            headers = {
                        'Authorization': 'Bearer ' + str(store_.token),
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                        }
            response = foodics_response(url, headers=headers, data=payload)
            save_foodics_invoices(response,store_, headers=headers, data=payload)
            print (response.json().get('links'))
            if response.json().get('links') :
                _next_url=response.json().get('links').get('next') + "&filter[business_date]="+ str(business_date) + "&filter[branch_id]=" + str(store_.branch_id)
                while _next_url :
                    print (_next_url)
                    time.sleep(2)  # Pause for 2 seconds
                    response = foodics_response(_next_url, headers=headers, data=payload)
                    save_foodics_invoices(response,store_, headers=headers, data=payload)
                    _next_url = response.json().get('links').get('next')
                    if _next_url :
                        _next_url = response.json().get('links').get('next') + "&filter[business_date]="+ str(business_date) + "&filter[branch_id]=" + str(store_.branch_id)


            #print(response.json())




            #print(store_.store_name)