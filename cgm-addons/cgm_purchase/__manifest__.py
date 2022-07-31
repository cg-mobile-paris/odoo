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
    ],
    'data': [
        # data
        'data/ir_sequence_data.xml',
        # security
        'security/ir.model.access.csv',
        # report
        'report/need_mgmt_process_report.xml',
        'report/need_mgmt_process_report_templates.xml',
        # views
        'views/need_mgmt_process_views.xml',
        'views/need_mgmt_process_line_views.xml',
        'views/ir_ui_menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
