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
            self.DB, self.UID, self.PASS, model, 'create', datas
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

    def search(self, model, domain=False, order=False, limit=False):
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


con_odoo_us = ConOdoo(
            db="cgmobile-master-preprod-11601718",
            user="platform@cg-mobile.com",
            password="platform@cg-mobile.com",
            port=443,
            url="https://cgmobile-master-preprod-11601718.dev.odoo.com"
        )

con_odoo_dest = ConOdoo(
            db="cg-mobile-paris-merge",
            user="admin@cg-mobile.com",
            password="admin@cg-mobile.com",
            port=8069,
            url="http://127.0.0.1"
        )

print(con_odoo_us)
print(con_odoo_dest)

def search_ref(model, name):
    res = con_odoo_dest.search(model, [[['name','=', name]]])
    print(model, name, res)
    return res[0] if res else False

def find_product_us(product_id_us):
    product_us = con_odoo_us.read("product.product", [product_id_us], ['barcode'])
    if product_us:
        product_id = con_odoo_dest.search_read("product.product", [[['barcode', '=', product_us[0]['barcode']]]], ['id'])
        if product_id:
            return product_id[0]['id']
        else:
            product_us = con_odoo_us.read("product.product", [product_id_us], ['default_code'])
            if product_us:
                product_id = con_odoo_dest.search_read("product.product",[[['default_code', '=', product_us[0]['default_code']]]], ['id'])
                if product_id:
                    return product_id[0]['id']


def main():
    # REPRISE DES ACHATS
    # GET CG Mobile France SAS ID 127.0.0.1
    cg_mobile_fr_id = 1
    cg_mobile_fr_in_us_id = 1143
    # GET Purchase with cg_mobile_fr_in_us_id
    po_fields = ['partner_ref', 'currency_id', 'date_approve', 'date_planned',
                 'delivery_status', 'invoice_status', 'origin', 'name',
                'order_line',
                'company_id', 'picking_type_id']
    product_line_fields = ['product_id', 'name', 'product_qty', 'price_unit']

    po_ids = con_odoo_us.search_read(
        "purchase.order",
        [[
            ['partner_id', '=', cg_mobile_fr_in_us_id],
            ['state', '=', 'purchase'],
            ['delivery_status', '=', 'done'],
            ['invoice_status', '=', 'invoiced'],
          ]],
        fields=po_fields
    )
    # print(po_ids)
    for po_id in po_ids:
        if not con_odoo_dest.search("purchase.order", [[['name', '=', po_id["name"]]]]):
            po_vals_line_list = []
            pl_ids = con_odoo_us.read(
                "purchase.order.line",
                po_id['order_line'],
                fields=product_line_fields
            )
            for pl_id in pl_ids:
                po_vals_line = (0, 0, {
                    "product_id": find_product_us(pl_id["product_id"][0]),
                    "name": pl_id["name"],
                    "product_qty": pl_id["product_qty"],
                    "qty_received": pl_id["product_qty"],
                    "qty_invoiced": pl_id["product_qty"],
                    "qty_to_invoice": 0.0,
                    "price_unit": pl_id["price_unit"],
                    "state": "purchase"
                })
                po_vals_line_list.append(po_vals_line)
            po_vals = {
                "name": po_id["name"],
                "partner_ref": po_id["partner_ref"],
                "partner_id": cg_mobile_fr_id,
                "origin": po_id["origin"],
                "currency_id": 2,
                "date_approve": po_id["date_approve"],
                "date_planned": po_id["date_planned"],
                "delivery_status": po_id["delivery_status"],
                "invoice_status": po_id["invoice_status"],
                "company_id": 2,
                "order_line": po_vals_line_list,
                "state": "purchase"
            }

            try :
                po_id_create = con_odoo_dest.create("purchase.order", [po_vals])
                con_odoo_dest.write("purchase.order", po_id_create, {"invoice_status": "invoiced"})
            except:
                print(po_vals)

main()