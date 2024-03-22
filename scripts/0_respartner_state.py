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
    # REPRISE PARTNER
    state_ids = con_odoo_us.search_read(
        "res.country.state",
        [[['name', '!=', '']]],
        fields=['name', 'code', 'ice_mobility_code', 'country_id']
    )
    for state_id in state_ids:
        state_dest = con_odoo_dest.search_read(
            'res.country.state', [[['name', '=', state_id['name']]]],
        )

        print(state_id)
        print(state_dest)

        vals = {
            "code": state_id["code"],
            "ice_mobility_code": state_id["ice_mobility_code"],
        }
        if state_dest:
            con_odoo_dest.write("res.country.state", state_dest[0]["id"], vals)
        else:

            vals['name'] = state_id["name"]
            vals['country_id'] = con_odoo_dest.search(
                "res.country",
                [[['name', '=', state_id['country_id'][1]]]]
            )[0]
            print(vals)
            try:
                con_odoo_dest.create("res.country.state", [vals])
            except:
                pass



main()