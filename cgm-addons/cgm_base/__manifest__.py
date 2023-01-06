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
        'views/res_bank_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cgm_base/static/src/legacy/js/fields/form_view.js',
        ]
    },
    'application': False,
    'installable': True,
    'auto_install': False,
}
