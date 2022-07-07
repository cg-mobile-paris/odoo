# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE SALE',
    'summary': '',
    'category': 'Sales',
    'version': '15.0.0.1',
    'sequence': -97,
    'author': 'ArkeUp',
    'license': 'AGPL-3',
    'website': 'https://arkeup.com',
    'description': '',
    'depends': [
        'cgm_base',
        'sale_management',
        'sale_order_line_product_image',
    ],
    'data': [
        # data
        # security
        'security/ir.model.access.csv',
        # views
        'views/product_collection_view.xml',
        'views/product_template_view.xml',
        'views/ir_ui_menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
