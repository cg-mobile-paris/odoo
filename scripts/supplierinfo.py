import xmlrpc.client


class ConOdoo:
    def __init__(self, url, port, db, user, password):
        self.DB = db
        self.USER = user
        self.PASS = password
        self.PORT = port
        self.URL = url
        self.URL_COMMON = f"{self.URL}:{self.PORT}/xmlrpc/2/common"
        self.URL_OBJECT = f"{self.URL}:{self.PORT}/xmlrpc/2/object"
        self.ODOO_COMMON = xmlrpc.client.ServerProxy(self.URL_COMMON)
        self.ODOO_OBJECT = xmlrpc.client.ServerProxy(self.URL_OBJECT)
        self.UID = self.ODOO_COMMON.authenticate(self.DB, self.USER, self.PASS, {})

    def create(self, model, datas):
        return self.ODOO_OBJECT.execute_kw(
            self.DB, self.UID, self.PASS, model, 'create', [datas]
        )

    def write(self, model, ids, datas):
        return self.ODOO_OBJECT.execute_kw(self.DB, self.UID, self.PASS, model, 'write', [ids, datas])

    def read(self, model: object, ids: object, fields: object = False) -> object:
        if fields:
            return self.ODOO_OBJECT.execute_kw(
                self.DB, self.UID, self.PASS, model, 'read', [ids], {'fields': fields}
            )
        else:
            return self.ODOO_OBJECT.execute_kw(
                self.DB, self.UID, self.PASS, model, 'read', [ids],
            )

    def search_read(self, model, domain=False, fields=False, order=False, limit=False):
        params = {}
        if not domain:
            domain = []
        if fields:
            params['fields'] = fields
        if order:
            params['order'] = order
        if limit:
            params['limit'] = limit

        return self.ODOO_OBJECT.execute_kw(
            self.DB, self.UID, self.PASS, model, 'search_read', domain, params
        )

    def search(self, model, domain= False, order=False, limit=False):
        params = {}
        if not domain:
            domain = []
        if order:
            params['order'] = order
        if limit:
            params['limit'] = limit
        return self.ODOO_OBJECT.execute_kw(
            self.DB, self.UID, self.PASS, model, 'search', domain, params
        )

    def read_group(self, model, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        return self.ODOO_OBJECT.execute_kw(
            self.DB, self.UID, self.PASS, model, 'read_group', domain, {'fields': fields, 'groupby': groupby}
        )



con_odoo_fr = ConOdoo(
            db="cg-mobile-preprod-12287988",
            user="admin@cg-mobile.com",
            password="admin@cg-mobile.com",
            port=443,
            url="https://cg-mobile-preprod-12287988.dev.odoo.com"
        )

con_odoo_us = ConOdoo(
            db="cgmobile-master-preprod-11601718",
            user="platform@cg-mobile.com",
            password="platform@cg-mobile.com",
            port=443,
            url="https://cgmobile-master-preprod-11601718.dev.odoo.com"
        )

con_odoo_dest = ConOdoo(
            db="cg-mobile-paris17",
            user="admin@cg-mobile.com",
            password="admin@cg-mobile.com",
            port=8069,
            url="http://127.0.0.1"
        )

print(con_odoo_fr)
print(con_odoo_us)
print(con_odoo_dest)

def main():
    #  'CG Mobile PriceList'
    pricelist_names = ['PriceList (B2B)']
    # REPRISE DES LISTE DE PRIX
    for pricelist_name in pricelist_names:
        price_list_datas = []

        pricelist_us_d = con_odoo_us.search_read(
            model='product.pricelist',
            domain=[[('name', '=', pricelist_name)]],
            fields=['name']
        )
        items = con_odoo_us.search_read(
            model='product.pricelist.item',
            domain=[[('pricelist_id', '=', pricelist_us_d[0]['id'])]],
            fields=['pricelist_id', 'product_id', 'currency_id', 'company_id', 'compute_price', 'min_quantity', 'date_start', 'date_end', 'fixed_price']
        )
        n_items = len(items)
        for i, item in enumerate(items):
            print(item)
            perc = round((i * 100) / n_items, 2)
            print(perc, "% /", n_items)
            product_us_id = con_odoo_us.read(
                "product.product",
                [item['product_id'][0]],
                ['barcode', 'product_tmpl_id']
            )
            barecode_us = product_us_id[0]['barcode']
            product_id = con_odoo_dest.search(
                "product.product",
                [[('barcode', '=', barecode_us)]],
            )
            if product_id:
                vals = {
                    "product_id": product_id[0],
                    "currency_id": 2,
                    "company_id": 2,
                    "compute_price": item["compute_price"],
                    "min_quantity": item["min_quantity"],
                    "date_start": item["date_start"],
                    "date_end": item["date_end"],
                    "fixed_price": item["fixed_price"],

                }
                print(vals)
                price_list_datas.append((0, 0, vals))
        con_odoo_dest.create("product.pricelist",
                             {
                                        "item_ids": price_list_datas,
                                        "name": pricelist_name,
                                        "currency_id": 2,
                                        "company_id": 2,
                              })

# fields = ['product_id', 'currency_id', 'company_id', 'compute_price',
#           'min_quantity', 'date_start', 'date_end', 'fixed_price']
main()