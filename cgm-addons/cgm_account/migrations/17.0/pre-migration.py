# -*- coding: utf-8 -*-
from odoo.upgrade import util

def delete_views(env):
    view_list = [
        'base.module_arkeup_background_image',
        'base.module_purchase_reception_status',
        'base.module_sale_delivery_state',
        # 'base.module_smile_api_rest',
        'cgm_account.view_move_line_tree',
        'cgm_account.action_account_move_line',
        'cgm_account.account_move_view_tree_inherit',
        'cgm_sale.report_sale_order_document_inherit',
        'cgm_sale.report_saleorder_document_inherit',
        'cgm_base.res_bank_form_inherit',
        'cgm_base.cg_mobile_web_layout',
        'sale_delivery_state.view_order_tree_inherit_delivery_state',
        'sale_delivery_state.view_quotation_tree_inherit_delivery_state',
        'sale_delivery_state.view_order_form_inherit_delivery_state',
        'purchase_reception_status.purchase_order_form',
        'purchase_reception_status.view_purchase_order_filter',
        'purchase_reception_status.purchase_order_tree',
        'purchase_reception_status.purchase_order_view_tree',
        'smile_api_rest.model_api_rest_field',
        'smile_api_rest.model_api_rest_function_parameter',
        'smile_api_rest.model_api_rest_log',
        'smile_api_rest.model_api_rest_path',
        'smile_api_rest.model_api_rest_tag',
        'smile_api_rest.model_api_rest_version',
        'smile_api_rest.menu_api_rest',
        'smile_api_rest.menu_action_api_rest_version',
        'smile_api_rest.menu_action_api_rest_path',
        'smile_api_rest.menu_api_rest_configuration',
        'smile_api_rest.menu_action_api_rest_tag',
    ]


    for v in view_list:
        print('odoo: delete_views', v)
        util.records.remove_record(env, v)

def manage_modules(env):
    modules = ['smile_api_rest', 'api_rest', 's2u_oauth2', 'sale_delivery_state', 'purchase_reception_status']
    for m in modules:
        print('odoo: manage_modules', m)
        util.uninstall_module(env, m)
        util.remove_module(env, m)

def migrate(cr, version):
    print('MIGRATE')
    manage_modules(cr)
    delete_views(cr)

