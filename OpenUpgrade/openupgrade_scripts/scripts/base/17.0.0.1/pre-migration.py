# Copyright 2020 Odoo Community Association (OCA)
# Copyright 2020 Opener B.V. <stefan@opener.am>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from openupgradelib import openupgrade
from odoo import tools

_logger = logging.getLogger(__name__)

# from modules.cgmobileparis.OpenUpgrade.openupgrade_scripts.apriori import ...
# from ...OpenUpgrade.openupgrade_scripts.apriori import merged_modules, renamed_modules, renamed_models, merged_models, renamed_tables



def delete_views(env):
    view_list = [
        'view_move_line_tree',
        'action_account_move_line',
        'account_move_view_tree_inherit',
        'report_sale_order_document_inherit',
        'report_saleorder_document_inherit',
        'res_bank_form_inherit',
        'cg_mobile_web_layout',

    ]
    print('delete_views !!!')

    openupgrade.delete_records_safely_by_xml_id(env, view_list)

def rename_user(env):
    get_data_query = """UPDATE res_users SET password = 'admin' WHERE login = 'admin@cg-mobile.com';"""
    env.cr.execute(get_data_query)
    get_data_query = """UPDATE res_users SET login = 'admin' WHERE login = 'admin@cg-mobile.com';"""
    env.cr.execute(get_data_query)

@openupgrade.migrate()
def migrate(env, version):
    """
    Don't request an env for the base pre-migration as flushing the env in
    odoo/modules/registry.py will break on the 'base' module not yet having
    been instantiated.
    """
    if "openupgrade_framework" not in tools.config["server_wide_modules"]:
        logging.error(
            "openupgrade_framework is not preloaded. You are highly "
            "recommended to run the Odoo with --load=openupgrade_framework "
            "when migrating your database."
        )

    delete_views(env)
    rename_user(env)
