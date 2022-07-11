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
        'data/product_form_data.xml',
        'data/product_licence_data.xml',
        'data/product_material_data.xml',
        # security
        'security/ir.model.access.csv',
        # views
        'views/product_form_views.xml',
        views/product_licence_views.xml,
        'views/product_material_views.xml',
        'views/product_template_views.xml',
        'views/ir_ui_menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
