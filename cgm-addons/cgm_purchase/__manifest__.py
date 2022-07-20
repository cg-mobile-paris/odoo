# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE PURCHASE',
    'summary': '',
    'category': 'Purchase',
    'version': '15.0.0.1',
    'sequence': -96,
    'author': 'ArkeUp',
    'license': 'AGPL-3',
    'website': 'https://arkeup.com',
    'description': '',
    'depends': [
        'purchase',
        'cgm_sale',
        'purchase_order_line_product_image',
    ],
    'data': [
        # security
        # data
        # report
        'report/purchase_templates.xml',
        'report/purchase_reports.xml',
        # views
        'views/purchase_order_views.xml',
        'views/ir_ui_menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
