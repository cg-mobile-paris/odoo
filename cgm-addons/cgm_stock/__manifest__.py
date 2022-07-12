# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE STOCK',
    'summary': '',
    'category': 'Inventory',
    'version': '15.0.0.1',
    'sequence': -95,
    'author': 'ArkeUp',
    'license': 'AGPL-3',
    'website': 'https://arkeup.com',
    'description': '',
    'depends': [
        'stock',
        'cgm_base',
    ],
    'data': [
        # security
        # data
        # views
        'views/stock_account_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
