# -*- coding: utf-8 -*-
from odoo import fields, models

class DeviceModel(models.Model):
    _name = "cgmobile.device_model"
    _description = "Device Model"
    _order = "brand_id, name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    brand_id = fields.Many2one('common.product.brand.ept', string='Brand')