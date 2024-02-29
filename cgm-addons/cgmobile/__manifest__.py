# -*- coding: utf-8 -*-
{
    'name': 'CG Mobile Customization',
    'version': '17.0',
    'author': 'Irokoo | Lilian Olivier',
    'website': 'https://www.irokoo.fr',
    'summary': 'Customize Odoo for CG Mobile',
    'description': """
CG Mobile Customization
=======================

Customize Odoo for CG Mobile

Features:
---------
* Add Sales Channel management for Shopify Odoo Connector.
    - Mapping between Shopify channel identifier (source_name) and Odoo Sales Team
    - At Import, automatically affect the right Sales Team to order according to the mapping


""",
    'depends': [
        'stock',
        'base_automation',
        'stock_barcode',
        'sale_amazon',
        'purchase',
    ],
    'data': [
        # SECURITY
        'security/ir.model.access.csv',
        'security/groups.xml',

        # DATAS
        # "datas/automated_actions.xml",
        # "datas/scheduled_actions.xml",

        # VIEWS
        "views/sale_order.xml",
        "views/document_layout.xml",
        "views/stock_move_line_views.xml",
        "views/purchase_views.xml",
        "views/product_template_views.xml",
        "views/product_views.xml",
        "views/product_color_views.xml",
        "views/product_category_views.xml",
        "views/product_sub_category_views.xml",
        "views/product_material_views.xml",
        "views/product_protection_level_views.xml",
        "views/product_collection_views.xml",
        "views/device_type_views.xml",
        "views/device_model_views.xml",
        "views/res_partner_views.xml",
        "views/ice_mobility_views.xml",
        "views/sales_team_views.xml",
        "views/amazon_marketplace_views.xml",

        # REPORT
        # "views/report_invoice.xml",
        # "views/report_purchase.xml",
        # "views/report_pdf_file.xml", #fixme v17 : ?

    ],
    'installable': True,
    'auto_install': False,
}
