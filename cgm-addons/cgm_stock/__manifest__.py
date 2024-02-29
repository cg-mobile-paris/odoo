# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE STOCK',
    'summary': '',
    'category': 'Inventory',
    'version': '17.0',
    'sequence': -96,
    'author': 'Irokoo | Lilian Olivier',
    'license': 'AGPL-3',
    'website': 'https://www.irokoo.fr',
    'description': '',
    'depends': [
        'stock',
        'cgm_base',
        # 'stock_picking_return_refund_option',
    ],
    'data': [
        # data
        # security
        'security/res_groups.xml',
        # report
        'report/report_deliveryslip.xml',
        'report/report_stock_reception.xml',
        # views
        'views/stock_picking_views.xml',
        'views/report_stockpicking_operations.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
