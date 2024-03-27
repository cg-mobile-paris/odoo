import xmlrpc.client
import pandas as pd

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
    cg_mobile_fr_id = 1
    cg_mobile_fr_in_us_id = 1143
    contact_df = pd.read_csv("b2b-contacts.csv")


    for i, c in contact_df.iterrows():
        contact_us_id = con_odoo_us.search(
            "res.partner",
            [[('name', '=', c['Display Name'])]]
        )
        contact_dest_id = con_odoo_dest.search(
            "res.partner",
            [[('name', '=', c['Display Name'])]],
        )
        print(contact_dest_id)

        ship_id = con_odoo_dest.search_read(
            "res.partner",
            [[('parent_id', '=', contact_dest_id[0]), ('type', '=', 'delivery')]],
            fields=['child_ids']
        )
        invoice_id = con_odoo_dest.search_read(
            "res.partner",
            [[('parent_id', '=', contact_dest_id[0]), ('type', '=', 'invoice')]],
            fields=['child_ids']
        )
        if not ship_id:
            ship_id = contact_dest_id[0]
        if not invoice_id:
            invoice_id = contact_dest_id[0]


        sale_ids = con_odoo_us.search_read(
            "sale.order",
            domain=[[('partner_id', '=', contact_us_id),
                     ('delivery_status', '=', 'done'),
                     ('invoice_status', '=', 'invoiced')]],
            fields=['name', 'partner_id', 'partner_shipping_id',
                   'partner_invoice_id', 'date_order',
                   'pricelist_id', 'payment_term_id', 'company_id',
                   'client_order_ref', 'order_line'])


        print(sale_ids)

        for sale_id in sale_ids:
            if not con_odoo_dest.search("sale.order", [[['name', '=', sale_id["name"]]]]):
                so_vals_line_list = []
                sale_order_line_ids = con_odoo_us.read(
                    "sale.order.line",
                    sale_id['order_line'],
                    fields=['product_id', 'name', 'product_uom_qty',
                            'qty_delivered', 'qty_invoiced', 'price_unit', ]
                )
                print("  ", sale_order_line_ids)

                for sale_line_id in sale_order_line_ids:
                    so_vals_line = (0, 0, {
                        "product_id": find_product_us(sale_line_id["product_id"][0]),
                        "name": sale_line_id["name"],
                        "product_uom_qty": sale_line_id["product_uom_qty"],
                        "qty_delivered": sale_line_id["qty_delivered"],
                        "qty_invoiced": sale_line_id["qty_invoiced"],
                        "delivery_status": "done",
                        "invoice_status": "invoiced",
                        "currency_id": 2,
                        "company_id": 2,
                        "state": "sale"
                    })
                    so_vals_line_list.append(so_vals_line)

                so_vals = {
                    "name": sale_id["name"],
                    "partner_id": contact_dest_id[0],
                    "partner_shipping_id": ship_id,
                    "partner_invoice_id": invoice_id,
                    "date_order": sale_id["date_order"],
                    "client_order_ref": sale_id["client_order_ref"],
                    "order_line": so_vals_line_list,
                }
                print(so_vals)
                #TODO voir si on prend saleperson, team, pricelist, paymenterm...
                # try :
                so_id_create = con_odoo_dest.create("sale.order", [so_vals])
                con_odoo_dest.write("sale.order", so_id_create,
                                    {"invoice_status": "invoiced",
                                           "delivery_status": "done"})
                # except Exception as e:
                #     print(e.faultString, so_vals)
main()