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
        # data
        # security
        'security/res_groups.xml',
        # report
        'report/report_deliveryslip.xml',
        # views
        'views/report_stockpicking_operations.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
