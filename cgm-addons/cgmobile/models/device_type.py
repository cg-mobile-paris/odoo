# -*- coding: utf-8 -*-
from odoo import fields, models

class DeviceType(models.Model):
    _name = "cgmobile.device_type"
    _description = "Device Type"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)