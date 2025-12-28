import frappe
import requests
import json
import time
from datetime import date, timedelta
from frappe.utils.password import get_decrypted_password
from frappe.utils import add_to_date, now_datetime


import psycopg2

def foodics_response(endpoint,data={},headers={}):
    response = requests.request("GET", endpoint, headers=headers, data=data)
    return response

def save_foodics_invoices(response,store_name,data={},headers={}):
    store_date = response.json().get('data')
    print (store_date)
    
    for date_item in store_date:
        #print ("save_foodics_invoices >>" , store_name)
        store_ = frappe.get_doc('Rental Integration Master', store_name)
        print ("save_foodics_invoices >>" , store_.store_name)
        #print (date_item['id'])
        new_si = frappe.new_doc("Rental Integration Sales")
        new_si.store = store_.name
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
            frappe.db.commit()
        except:
            pass
    
##bench --site site1.local execute egy_rent.tasks.pull_integration_invoices
##bench --site system.egygab.com execute egy_rent.tasks.pull_integration_invoices
@frappe.whitelist()
def pull_integration_invoices(business_date = date.today() - timedelta(days=1),store_code=None):
    #store_code=1
    print (str(store_code))
    if store_code:
        stores = frappe.db.get_all('Rental Integration Master',filters={'name': store_code ,'dont_import_data': False})
    else:
        stores = frappe.db.get_all('Rental Integration Master',filters={'dont_import_data': False })

    for store in stores:
        store_ = frappe.get_doc('Rental Integration Master', store.name)
        #print (store_.integration_type)
        ######################################################
        ################### foodics ##########################
        ######################################################
        if store_.integration_type == "foodics" :
            ################### foodics ##########################
            print ("store_.name", ">>>" , store_.store_name)
            print (store_.integration_type)
            url = "https://api.foodics.com/v5/orders?filter[business_date]=" + str(business_date) + "&filter[branch_id]=" + str(store_.branch_id)
            payload = {'charge_id': '9775780c-f713-453c-bf12-6c9245134c05'}
            headers = {
                        'Authorization': 'Bearer ' + str(store_.token),
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                        }
            response = foodics_response(url, headers=headers, data=payload)
            print (str(response.json()))
            save_foodics_invoices(response,store.name, headers=headers, data=payload)
            #print (response.json().get('links'))
            if response.json().get('links') :
                try:
                    _next_url=response.json().get('links').get('next') + "&filter[business_date]="+ str(business_date) + "&filter[branch_id]=" + str(store_.branch_id)
                except:
                    _next_url = None
                while _next_url :
                    #print (_next_url)
                    time.sleep(2)  # Pause for 2 seconds
                    response = foodics_response(_next_url, headers=headers, data=payload)
                    save_foodics_invoices(response,store.name, headers=headers, data=payload)
                    _next_url = response.json().get('links').get('next')
                    if _next_url :
                        _next_url = response.json().get('links').get('next') + "&filter[business_date]="+ str(business_date) + "&filter[branch_id]=" + str(store_.branch_id)

        if store_.integration_type == "PostgreSQL" :
            
            print (get_decrypted_password('Rental Integration Master',store.name,"db_password"))
            try:
            # Establish a connection to the PostgreSQL database
                conn = psycopg2.connect(
                    host= store_.db_host,          # Or your database host
                    database= store_.db_name,  # Replace with your database name
                    user= store_.db_username,      # Replace with your PostgreSQL username
                    password= get_decrypted_password('Rental Integration Master',store.name,"db_password"), # Replace with your PostgreSQL password
                    port= store_.db_port      # Optional: specify port if not default
                )
                cur = conn.cursor()
                _sql = str( store_.sql_view ) + "'" + str(business_date) + "'"
                print (_sql)
                cur.execute( _sql )
                invis = cur.fetchall()
                for inv in invis:
                    _external_id = str(store_.code) + "-" + str(inv[0])
                    print ("PostgreSQL" , " >> _external_id >>" , _external_id)
                    new_si = frappe.new_doc("Rental Integration Sales")
                    new_si.store = store_.name
                    new_si.external_id = _external_id
                    new_si.external_reference = str(inv[0])
                    new_si.invoice_date = business_date
                    new_si.net_amount = inv[2]
                    new_si.invoice_amount = inv[3]
                    new_si.external_type_name="Active"
                    try:
                        new_si.insert()
                        time.sleep(1)  # Pause for seconds
                    except:
                        pass

                    frappe.db.commit()

                frappe.db.commit()
                
            except psycopg2.Error as e:
                print(f"Error connecting to PostgreSQL: {e}")
            finally:
                # Close the cursor and connection
                if cur:
                    cur.close()
                if conn:
                    conn.close()
                print("Database connection closed.")                

    # print ("=============== >> " + str(business_date))
    #         #print(response.json())




            #print(store_.store_name)

@frappe.whitelist()
def pull_integration_invoices_dates(start_date=date.today() - timedelta(days=2),end_date=date.today() - timedelta(days=1),store_code=None):
    #delta = timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        print(current_date)
        #queue='short'
        frappe.enqueue('egy_rent.tasks.pull_integration_invoices', queue='default', business_date=current_date, store_code=store_code)
        #current_date += delta
        current_date = frappe.utils.add_to_date(current_date, days=1) 
    
