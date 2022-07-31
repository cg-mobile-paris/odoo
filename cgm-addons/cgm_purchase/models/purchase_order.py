# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    need_mgmt_process_id = fields.Many2one('need.mgmt.process', 'Need Mgmt Process', required=False)
