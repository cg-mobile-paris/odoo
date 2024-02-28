from openupgradelib import openupgrade



def try_delete_noupdate_records(env):
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "sale_delivery_state.view_order_tree_inherit_delivery_state",
            "sale_delivery_state.view_order_form_inherit_delivery_state",
        ],
    )


@openupgrade.migrate()
def migrate(env, version):
    try_delete_noupdate_records(env)