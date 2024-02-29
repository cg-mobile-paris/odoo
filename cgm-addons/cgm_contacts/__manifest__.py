# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE CONTACTS',
    'summary': '',
    'category': 'Sales/CRM',
    'version': '17.0',
    'sequence': -92,
    'author': 'Irokoo | Lilian Olivier',
    'license': 'AGPL-3',
    'website': 'https://www.irokoo.fr',
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
