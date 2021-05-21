import requests


# This is a python interface for the Mintsoft Swagger API: https://api.mintsoft.co.uk/swagger/ui/index#/
# It is still very much incomplete but you are able to get some order and product information
class Mintsoft():

    #Object Variables
    key = None

    def init(self):
        pass

    # returns API key for future API calls

    def auth(self, un, pw):
        payload = { "UserName": un, "Password": pw}
        base_url = "https://api.mintsoft.co.uk/api/Auth"
        r = requests.get(base_url, params=payload)
        self.key = r.json()


    #returns a list of orders as a list of dicts, if there are no orders that meet the criteria give, returns an empty list
    # status - order status code, check OrderStatus.py for different codes
    # pageno - the page you want to look at, pages start at 1
    # limit - number of items returned per page
    # ShowItems - Show the items associated with each order

    def get_order_list(self, status,  pageno, since=None, limit=100, ShowItems=True):
        payload = {"APIKey":self.key, "OrderStatusId":status, "PageNo":pageno, "Limit": limit, "SinceDate":since, "IncludeOrderItems":ShowItems}
        base_url = "https://api.mintsoft.co.uk/api/Order/List"
        r = requests.get(base_url, params=payload)
        return r.json()
        


    #returns a list of products as a list of dicts, if there are no products returns an empty list
    # pageno - the page you want to return
    # limit - number of items returned per page
    def get_product_list(self, pageno, limit=100):
        payload = {"APIKey":self.key, "PageNo":pageno, "Limit": limit}
        base_url = "https://api.mintsoft.co.uk/api/Product/List"
        r = requests.get(base_url, params=payload)
        return r.json()



    # returns all inventory information associated with the product as a 1 element list of dicts, if the ID does not exists, returns an empty list
    # product_id - ID of the product you want to look at
    def get_product_inv(self, product_id):
        payload = {"APIKey":self.key, "ID":product_id}
        url = "https://api.mintsoft.co.uk/api/Product/{}/Inventory?APIKey={}".format(payload["ID"], payload["APIKey"])
        r = requests.get(url)
        return r.json()

    # returns a list of all the product ids in your mintsoft system, if there are no products, returns an empty list
    def get_product_ids(self):
        pageno = 1

        product_list = self.get_product_list(pageno)
        product_ids = []

        while product_list != []:
            for item in product_list:
                if item['Weight'] > 0:
                    id_sku = (item['ID'] , item['SKU'])
                    product_ids.append(id_sku)

            pageno += 1

            product_list = self.get_product_list(pageno)

        return product_ids


    # returns all the orders with the specified status and after the specified data until right now
    # status - status code of the order, check OrderStatus.py
    # date - date to start from
    def get_orders(self, status, date):
        pageno = 1
        order_list = self.get_order_list(status=status, pageno=pageno, since=date)
        sku_backorder = {}

        while order_list != []:
            
            for order in order_list:
                order_items = order['OrderItems']
                for item in order_items:
                    sku = item['SKU']
                    on_BO = item['Quantity']

                    try:
                        sku_backorder[sku] += on_BO 
                    except KeyError: # key not in dict, so we need to add it
                        sku_backorder[sku] = on_BO 
            
            pageno += 1
            order_list = self.get_order_list(status=status, pageno=pageno, since=date)

        return sku_backorder