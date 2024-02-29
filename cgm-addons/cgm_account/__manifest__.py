# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE ACCOUNT',
    'summary': '',
    'category': 'Accounting',
    'version': '17.0',
    'sequence': -98,
    'author': 'Irokoo | Lilian Olivier',
    'license': 'AGPL-3',
    'website': 'https://www.irokoo.fr',
    'description': '',
    'depends': [
        'l10n_fr',
        'cgm_base',
        'account_accountant',
    ],
    'data': [
        # security
        'security/res_groups.xml',
        # views
        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
        # report
        'report/report_invoice.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
