# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE PURCHASE',
    'summary': '',
    'category': 'Purchase',
    'version': '17.0.0.1',
    'sequence': -96,
    'author': 'Irokoo | Lilian Olivier',
    'license': 'AGPL-3',
    'website': 'https://www.irokoo.fr',
    'description': '',
    'depends': [
        'purchase',
        'cgm_product',
        # 'purchase_reception_status'
    ],
    'data': [
        # data
        'data/ir_sequence_data.xml',
        # security
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        # report
        'report/need_mgmt_process_report.xml',
        'report/purchase_quotation_templates.xml',
        'report/need_mgmt_process_report_templates.xml',
        # views
        'views/need_mgmt_process_views.xml',
        'views/need_mgmt_process_line_views.xml',
        'views/purchase_order_line_views.xml',
        'views/purchase_order_views.xml',
        'views/ir_ui_menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
