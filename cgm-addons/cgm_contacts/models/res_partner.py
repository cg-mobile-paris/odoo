# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_royalties = fields.Boolean('Royalties', tracking=True)
    property_product_pricelist = fields.Many2one(tracking=True)
