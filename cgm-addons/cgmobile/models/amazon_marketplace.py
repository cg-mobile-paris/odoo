from odoo import exceptions, fields, models, _


class AmazonMarketplace(models.Model):
    _inherit = 'amazon.marketplace'

    # invoice partner
    fba_invoice_partner_id = fields.Many2one('res.partner', string='Invoice Partner', help='Partner to use for invoice')
    # default currency
    currency_id = fields.Many2one('res.currency', string='Currency', help='Currency to use for invoice')
    # payment journal
    payment_journal_id = fields.Many2one('account.journal', string='Payment Journal', help='Journal to use for payment', domain=[('type', 'in', ['bank', 'cash'])])
    # do not import tax
    do_not_import_tax = fields.Boolean(string='Do not import tax', help='Do not import tax from Amazon')
                                         