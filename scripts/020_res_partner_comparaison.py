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
#
# print(con_odoo_us)
# print(con_odoo_dest)

def search_ref(model, name):
    res = con_odoo_dest.search(model, [[['name','=', name]]])
    print(model, name, res)
    if res:
        return res[0]
    else:
        return False

def main_vendor():
    # REPRISE DES VENDEURS
    fixed_value_field = {'lang': 'en_US', 'company_id': 2, 'company_type': 'company'}
    fixed_field = ['name', 'street', 'street2', 'zip', 'country_id', 'phone', 'mobile', 'email', 'ref', 'city']
    other_field = ['state_id', 'property_product_pricelist']
    vendor_bill_ids = con_odoo_us.search_read(
        "res.partner",
        [[('supplier_rank','>', 0)]], fields=fixed_field + other_field
    )
    print(len(vendor_bill_ids))
    for v in vendor_bill_ids:
        # print(v['property_product_pricelist'][1])
        print(v)
        vals = {
            "name": v["name"],
            "street": v["street"],
            "street2": v["street2"],
            "zip": v["zip"],
            "country_id": search_ref("res.country", v["country_id"]),
            "state_id": search_ref("res.country.state", v["state_id"]),
            "property_product_pricelist": search_ref("product.pricelist", v["property_product_pricelist"][1]),
            "phone": v["phone"],
            "mobile": v["mobile"],
            "email": v["email"],
            "ref": v["ref"],
            "city": v["city"],
        }
        vals.update(fixed_value_field)
        print(vals)
        ref = search_ref("res.partner", v["name"])
        if not ref:
            con_odoo_dest.create("res.partner", [vals])
        else:
            con_odoo_dest.write("res.partner", ref,  vals)

def main_b2b_file():
    contact_df = pd.read_csv("b2b-contacts.csv")

    # REPRISE DES VENDEURS
    fixed_value_field = {'lang': 'en_US', 'company_id': 2, 'company_type': 'company'}
    fixed_field = ['name', 'street', 'street2', 'zip', 'country_id', 'phone', 'mobile', 'email', 'ref', 'city', 'type', 'company_type']
    other_field = ['state_id', 'property_product_pricelist']

    for i, c in contact_df.iterrows():
        contact_id = con_odoo_us.search_read(
            "res.partner",
            [[('name','=', c['Display Name'])]], fields=fixed_field + other_field + ['child_ids']
        )
        if not contact_id:
            pass
        else:
            v = contact_id[0]
            vals = {
                "name": v["name"],
                "street": v["street"],
                "street2": v["street2"],
                "zip": v["zip"],
                "country_id": search_ref("res.country", v["country_id"]),
                "state_id": search_ref("res.country.state", v["state_id"]),
                "property_product_pricelist": search_ref("product.pricelist", v["property_product_pricelist"][1]),
                "phone": v["phone"],
                "mobile": v["mobile"],
                "email": v["email"],
                "ref": v["ref"],
                "city": v["city"],
                "company_type": "company",
            }
            vals.update(fixed_value_field)

            child_ids = con_odoo_us.search_read(
                "res.partner",
                [[('id', 'in', v["child_ids"])]],
                fields=fixed_field + other_field + ['child_ids'])

            vals_child = []

            for c in child_ids:
                vals_c = {
                    "name": c["name"],
                    "street": c["street"],
                    "street2": c["street2"],
                    "zip": c["zip"],
                    "country_id": search_ref("res.country", c["country_id"]),
                    "state_id": search_ref("res.country.state", c["state_id"]),
                    "property_product_pricelist": search_ref("product.pricelist", v["property_product_pricelist"][1]),
                    "phone": c["phone"],
                    "mobile": c["mobile"],
                    "email": c["email"],
                    "ref": c["ref"],
                    "city": c["city"],
                    "type": c["type"],
                    "company_type": "person",
                }
                vals_child.append((0, 0, vals_c))

            vals.update({"child_ids": vals_child})
            print(vals)
            ref = search_ref("res.partner", v["name"])
            if not ref:
                con_odoo_dest.create("res.partner", [vals])
            else:
                con_odoo_dest.write("res.partner", ref, vals)


    # print(len(vendor_bill_ids))
    # for v in vendor_bill_ids:
    #     # print(v['property_product_pricelist'][1])
    #     print(v)
    #     vals = {
    #         "name": v["name"],
    #         "street": v["street"],
    #         "street2": v["street2"],
    #         "zip": v["zip"],
    #         "country_id": search_ref("res.country", v["country_id"]),
    #         "state_id": search_ref("res.country.state", v["state_id"]),
    #         "property_product_pricelist": search_ref("product.pricelist", v["property_product_pricelist"][1]),
    #         "phone": v["phone"],
    #         "mobile": v["mobile"],
    #         "email": v["email"],
    #         "ref": v["ref"],
    #         "city": v["city"],
    #     }
    #     vals.update(fixed_value_field)
    #     print(vals)
    #     ref = search_ref("res.partner", v["name"])
    #     if not ref:
    #         con_odoo_dest.create("res.partner", [vals])
    #     else:
    #         con_odoo_dest.write("res.partner", ref,  vals)
    #
main_b2b_file()