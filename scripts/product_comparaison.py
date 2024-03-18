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

print(con_odoo_fr)
print(con_odoo_us)

def create_list(datas, field):
    return [d[field] for d in datas if d[field]]



def main():
    # Sub Category us supprimer ?
    # product_protection_level_id
    convert_field = {
        'product_brand_id': 'brand_id',
        'product_color_id': 'color_id',
        'product_category_id': 'categ_id', #TODO a uniformiser
        'product_material_id': 'material_id',
        'product_collection_id': 'collection_id',
        'device_brand_id': 'licence_id',
        'device_model_id': 'device_id',
        'device_type_id': 'categ_id'

    }
    fix_field = {'detailed_type': 'product'}
    common_fields = ['name', 'invoice_policy', 'barcode', 'upc_code', 'standard_price', 'list_price', 'image_1920']
    product_fr_ids = con_odoo_fr.search_read(model="product.template", domain=[[('detailed_type', '=', 'product')]], fields=['barcode'])
    product_us_ids = con_odoo_us.search_read(model="product.template", domain=[[('type', '=', 'product')]], fields=['barcode'])
    barcode_fr = create_list(product_fr_ids, "barcode")
    barcode_us = create_list(product_us_ids, "barcode")
    print('barcode_fr', len(barcode_fr))
    print('barcode_us', len(barcode_us))
    diff_fr_us = set(barcode_fr) - set(barcode_us) #
    diff_us_fr = set(barcode_us) - set(barcode_fr)
    common_us_fr = set(barcode_us) & set(barcode_fr)
    print('common_us_fr', len(common_us_fr))

    # print('barcode non existant chez US')
    # print(len(diff_fr_us))
    # print(diff_fr_us)

    print('barcode non existant chez FR, a reprendre chez US')
    print(len(diff_us_fr))
    print(diff_us_fr)


main()