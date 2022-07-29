# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE ACCOUNT',
    'summary': '',
    'category': 'Accounting',
    'version': '15.0.0.1',
    'sequence': -98,
    'author': 'ArkeUp',
    'license': 'AGPL-3',
    'website': 'https://arkeup.com',
    'description': '',
    'depends': [
        'l10n_fr',
        'cgm_base',
        'account_accountant',
    ],
    'data': [
        # report
        'report/report_invoice.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
