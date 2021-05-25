from datetime import datetime, timedelta
from config import USERNAME_L, PASS_L, USERNAME_V, PASS_V, AIRTABLE_KEY, BASE_KEY, TABLE_L, TABLE_V
from OrderStatus import OrderStatus
from tqdm import tqdm
import json
from airtable import Airtable
from mintsoft import Mintsoft
import sys


def main(argv):

    try:
        site = argv[1]
    except IndexError:
        print("USAGE: main.py [venlo | livi]")
        quit()

    mintsoft = Mintsoft()

    if site == "livi":
        mintsoft.auth(un=USERNAME_L, pw=PASS_L)
        TABLE = TABLE_L
    if site == "venlo":
        TABLE = TABLE_V
        mintsoft.auth(un=USERNAME_V, pw=PASS_V)


    yesterday = (datetime.now() - timedelta(days=1))
    #format date and time to ISO standard so mintsoft likes it
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()


    print("getting stock sold yesterday")
    sold_yesterday =  mintsoft.get_orders(OrderStatus.NEW, yesterday)

    print("getting product IDs")
    product_ids =  mintsoft.get_product_ids() # get all the product IDs and SKUs

    full_list = []

    print("getting onhand and backorder info per sku...")
    for p_id, p_sku in tqdm(product_ids):

        try:
            product_inv = mintsoft.get_product_inv(p_id)[0]        
        except IndexError:
            continue

        on_hand = product_inv["OnHand"]
        back_orders = product_inv["RequiredByBackOrder"]
        try:
            sold =  sold_yesterday[p_sku]
        except KeyError:
            sold = 0

        #TODO add condition that ignore the SKU if all the fields are 0
        buffer = {  "SKU_TEXT": p_sku,
                    "SOLD YESTERDAY": sold,
                    "ONHAND": on_hand,  
                    "BACKORDERS": back_orders}
        full_list.append(buffer)

    print("updating airtable with new information")
    airtable = Airtable(BASE_KEY, TABLE, AIRTABLE_KEY)

    for item in tqdm(full_list):
        
        try:
            record = airtable.match('SKU_TEXT', item['SKU_TEXT'])
            if record == {}:
                airtable.insert(item)
            else:
                airtable.update(record['id'], item)
        except TypeError: #TODO actually handle the exceptions in the future but this should be okay for now
            print(item)
            continue


if __name__ == "__main__":
    main(sys.argv)

