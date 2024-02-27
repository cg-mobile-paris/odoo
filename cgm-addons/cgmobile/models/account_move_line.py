# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    avg_purchase_price = fields.Float(compute='_compute_avg_purchase_price', string='Average Purchase Price', compute_sudo=True, store=True)
    last_purchase_price = fields.Float(string="Last Purchase Price", compute="_compute_last_purchase_price", compute_sudo=True, store=True)

    @api.depends("product_id", "move_id.state")
    def _compute_last_purchase_price(self):
        for rec in self:
            if rec.product_id:
                last_purchase_price = (
                    self.env["purchase.order.line"]
                    .search(
                        [
                            ("company_id", "=", rec.company_id.id),
                            ("product_id", "=", rec.product_id.id),
                            ("order_id.state", "in", ["purchase", "done"]),
                        ],
                        order="id desc",
                        limit=1,
                    )
                    .price_unit
                )
                rec.last_purchase_price = last_purchase_price

    @api.depends('product_id', 'company_id', 'move_id.state')
    def _compute_avg_purchase_price(self):
        for line in self:
            if not line.product_id:
                line.avg_purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)
            product = line.product_id
            product_cost = product.standard_price
            if not product_cost:
                if not line.avg_purchase_price:
                    line.avg_purchase_price = 0.0
            else:
                line.avg_purchase_price = product_cost

    def _get_computed_account(self):
        """ 
        This method is used to get the account to use in case the account is not set on the account.move.line.
        Override this method to change the account to use in case the account is not set on the account.move.line.
        """
        account_id = super(AccountMoveLine, self)._get_computed_account()

        if self.move_id.is_sale_document(include_receipts=True):
            # Out invoice.
            # get sale order and check if it has a sales team
            # if it has a sales team, get the sales journal and use it as the account
            # if it doesn't have a sales team, use the default account
            if self.move_id.team_id and self.move_id.team_id.sales_journal_id:
                account_id = self.move_id.team_id.sales_journal_id.default_account_id or account_id

        return account_id
    