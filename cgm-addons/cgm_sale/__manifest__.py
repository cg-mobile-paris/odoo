# -*- coding: utf-8 -*-
{
    'name': 'CG-MOBILE SALE',
    'summary': '',
    'category': 'Sales',
    'version': '15.0.0.1',
    'sequence': -97,
    'author': 'ArkeUp',
    'license': 'AGPL-3',
    'website': 'https://arkeup.com',
    'description': '',
    'depends': [
        'cgm_base',
        'sale_management',
        'sale_order_line_product_image',
    ],
    'data': [
        # data
        'data/product_form_data.xml',
        'data/product_material_data.xml',
        'data/product_licence_data.xml',
        'data/product_category_data.xml',
        'data/product_device_data.xml',
        'data/product_brand_data.xml',
        'data/product_color_data.xml',
        # security
        'security/ir.model.access.csv',
        # report
        'report/sale_report_templates.xml',
        # views
        'views/product_form_views.xml',
        'views/product_material_views.xml',
        'views/product_licence_views.xml',
        'views/product_collection_views.xml',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'views/product_device_views.xml',
        'views/product_brand_views.xml',
        'views/product_color_views.xml',
        'views/sale_order_template_views.xml',
        'views/ir_ui_menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
