# -*- coding: utf-8 -*-
from odoo import fields, models


class SalesTeam(models.Model):
    _inherit = 'crm.team'

    # add a sales journal field to associate with the sales team
    sales_journal_id = fields.Many2one('account.journal', string='Sales Journal', domain=[('type', '=', 'sale')])
    # add fiscal position field to associate with the sales team
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')

    
