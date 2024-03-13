# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE SALE',
    'summary': '',
    'category': 'Sales',
    'version': '17.0',
    'sequence': -97,
    'author': 'Irokoo | Lilian Olivier',
    'license': 'AGPL-3',
    'website': 'https://www.irokoo.fr',
    'description': '',
    'depends': [
        'sales_team',
        'cgm_purchase',
        'sale_management',
        # 'sale_delivery_state',
        'currency_rate_live',
    ],
    'data': [
        # security
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        # report
        # 'report/stock_state_template.xml',
        # 'report/sale_report.xml',
        # 'report/sale_report_templates.xml',
        # views
        'views/sale_order_views.xml',
        'views/report_sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/sale_order_template_views.xml',
        'views/product_move_report_views.xml',
        'views/ir_ui_menu.xml',
        # data
        'data/mail_template_data.xml',

        #dash report
        'report/sale_report_view.xml',

    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
