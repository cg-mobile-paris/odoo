# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE BASE',
    'summary': '',
    'category': 'Tools',
    'version': '15.0.0.1',
    'sequence': -99,
    'author': 'ArkeUp',
    'license': 'AGPL-3',
    'website': 'https://arkeup.com',
    'description': '',
    'depends': [
        'web',
        'contacts',
        'report_xlsx',
    ],
    'data': [
        # data
        # security
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        # views
        'views/templates.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
