# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE CONTACTS',
    'summary': '',
    'category': 'Sales/CRM',
    'version': '15.0.0.1',
    'sequence': -92,
    'author': 'ArkeUp',
    'license': 'AGPL-3',
    'website': 'https://arkeup.com',
    'description': '',
    'depends': [
        'cgm_base',
    ],
    'data': [
        # security
        'security/res_groups.xml',
        # views
        'views/res_partner_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
