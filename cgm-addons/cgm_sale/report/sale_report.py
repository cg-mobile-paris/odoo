
from odoo import fields, models

class SaleReport(models.Model):
    _inherit = "sale.report"

    form_id = fields.Many2one(comodel_name='product.form', readonly=True)
    licence_id = fields.Many2one(comodel_name='product.licence', readonly=True)
    material_id = fields.Many2one(comodel_name='product.material', readonly=True)
    collection_id = fields.Many2one(comodel_name='product.collection', readonly=True)
    device_id = fields.Many2one(comodel_name='product.device', readonly=True)
    brand_id = fields.Many2one(comodel_name='product.brand', readonly=True)
    color_id = fields.Many2one(comodel_name='product.color', readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["form_id"] = "t.form_id"
        res["licence_id"] = "t.licence_id"
        res["material_id"] = "t.material_id"
        res["collection_id"] = "t.collection_id"
        res["device_id"] = "t.device_id"
        res["brand_id"] = "t.brand_id"
        res["color_id"] = "t.color_id"
        return res

    def _group_by_sale(self):
        group_by = super()._group_by_sale()
        group_by = f"""
            {group_by},
            t.form_id,
            t.licence_id,
            t.material_id,
            t.collection_id,
            t.device_id,
            t.brand_id,
            t.color_id
            """
        return group_by