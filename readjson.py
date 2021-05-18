import requests

from config import *
import datetime
ON_BACK_ORDER = 9


def get_API_key():
    payload = { "UserName": USERNAME, "Password": PASS}
    base_url = "https://api.mintsoft.co.uk/api/Auth"
    r = requests.get(base_url, params=payload)
    return r.json()



#get recent back orders
def get_orders(key, status, date):
    payload = {"APIKey":key, "OrderStatusId":status }
    base_url = "https://api.mintsoft.co.uk/api/Order/List"
    r = requests.get(base_url, params=payload)
    return r




def main():
    
    key = get_API_key()

    date_prev = datetime.datetime.now()

    print(date_prev)




if __name__ == "__main__":
    main()