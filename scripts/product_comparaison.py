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
        return self.ODOO_OBJECT.execute_kw(
            self.DB, self.UID, self.PASS, model, 'write', [ids, datas]
        )

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

def migrate_attributes():
    files = [
        ("product_device.csv", "product.device"),
        ("product_form.csv", "product.form"),
        ("product_material.csv", "product.material"),
        ("product_color.csv", "product.color"),
        ("product_licence.csv", "product.licence"),
        ("product_brand.csv", "product.brand"),
    ]
    for file in files:
        print(file)
        df = pd.read_csv(file[0])
        for i, r in df.iterrows():
            print(r['fr'])
            data_exist = con_odoo_dest.search_read(
                model=file[1],
                domain=[[('name', '=', r['fr'])]],
                fields=['name']
            )
            print(data_exist)
            if not data_exist:
                con_odoo_dest.create(
                    model=file[1],
                    datas=[{'name': r['fr']}]
                )

def create_list(datas, field):
    return [d[field] for d in datas if d[field]]

def remove_id_key(datas):
    del datas['id']
    return datas

def add_fix_field(datas, fix_field):
    for k, v in fix_field.items():
        datas[k] = v
    return datas

def add_converted_field(datas, convert_field):
    return datas

def main():

    migrate_attributes()

    convert_field = {
        # "categ_id": (["device_type_id", "product_category_id"],),
        "device_id": ("device_model_id", "product_device.csv"),

        "form_id": ("product_sub_category_id", "product_form.csv"),
        "material_id": ("product_material_id", "product_material.csv"),
        "color_id": ("product_color_id", "product_color.csv"),
        "licence_id": ("product_brand_id", "product_licence.csv"),
        "brand_id": ("device_brand_id", "product_brand.csv"),
        "collection_id": ("product_collection_id", False),
    }
    fix_field = {'detailed_type': 'product'}
    common_fields = ['name', 'invoice_policy', 'barcode', 'upc_code', 'standard_price', 'list_price',]

    product_fr_ids = con_odoo_fr.search_read(model="product.template", domain=[[('detailed_type', '=', 'product')]], fields=['barcode'])
    product_us_ids = con_odoo_us.search_read(model="product.template", domain=[[('type', '=', 'product')]], fields=['barcode'])
    barcode_fr = create_list(product_fr_ids, "barcode")
    barcode_us = create_list(product_us_ids, "barcode")

    print('barcode_fr', len(barcode_fr))
    print('barcode_us', len(barcode_us))
    diff_fr_us = set(barcode_fr) - set(barcode_us)
    diff_us_fr = set(barcode_us) - set(barcode_fr)
    common_us_fr = set(barcode_us) & set(barcode_fr)
    print('diff_fr_us', len(diff_fr_us))
    print('diff_us_fr', len(diff_us_fr))
    print('common_us_fr', len(common_us_fr))

    # 14 vers 15 / US vers FR
    for p_id in diff_us_fr:
        print(p_id)
        p_us_id = con_odoo_us.search_read(
            model="product.template",
            domain=[[('barcode', '=', p_id)]],
            fields=common_fields
        )[0]
        data = remove_id_key(p_us_id)
        data = add_fix_field(data, fix_field)
        # data = add_converted_field(data, convert_field)
        print(data)
main()