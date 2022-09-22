# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models


class ProductMoveReport(models.Model):
    _name = 'product.move.report'
    _description = 'Product Move Analysis Report'
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    user_id = fields.Many2one('res.users', 'User', readonly=True)
    nature = fields.Selection([('purchase_entry', 'Purchase Entry'),
                               ('sale_outlet', 'Sale Outlet')], string='Nature', readonly=True)
    name = fields.Char('Order Reference', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_name = fields.Char('Product Label')
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', readonly=True)
    licence_id = fields.Many2one('product.licence', 'Licence', readonly=True)
    product_uom_qty = fields.Float('Product Qty', readonly=True)
    price_subtotal = fields.Float('Untaxed Total', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Done'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True)

    def _select_sale(self, fields=None):
        if not fields:
            fields = {}
        select_ = """
            sol.id as id,
            so.user_id, 
            so.date_order as date, 
            so.name, 
            so.warehouse_id, 
            so.partner_id, 
            sol.product_id, 
            prtmpl.name as product_name,
            - sol.product_uom_qty AS product_uom_qty, 
            - sol.price_subtotal AS price_subtotal, 
            so.company_id, 
            prtmpl.licence_id, 
            'sale_outlet' AS nature, 
            sol.state
        """
        for field in fields.values():
            select_ += field
        return select_

    def _select_purchase(self, fields=None):
        if not fields:
            fields = {}
        select_ = """
            pol.id as id,
            po.user_id, 
            pol.date_planned as date, 
            po.name, 
            stpkt.warehouse_id, 
            po.partner_id, 
            pol.product_id, 
            prtmpl.name as product_name,
            pol.product_uom_qty, 
            pol.price_subtotal, 
            po.company_id, 
            prtmpl.licence_id, 
            'purchase_entry' as nature, 
            pol.state
        """
        for field in fields.values():
            select_ += field
        return select_

    def _from_sale(self, from_clause=''):
        from_ = """
            sale_order so, 
            sale_order_line sol, 
            product_product pr, 
            product_template prtmpl 
            %s
        """ % from_clause
        return from_

    def _from_purchase(self, from_clause=''):
        from_ = """
            purchase_order po, 
            purchase_order_line pol, 
            product_product pr, 
            product_template prtmpl,
            stock_picking_type stpkt
            %s
        """ % from_clause
        return from_

    def _where_sale(self, where_clause=''):
        where_ = """
            sol.order_id = so.id 
            AND 
            sol.product_id = pr.id 
            AND 
            pr.product_tmpl_id = prtmpl.id 
            AND 
            sol.display_type IS NULL 
            AND 
            product_id IS NOT NULL
            %s
        """ % where_clause
        return where_

    def _where_purchase(self, where_clause=''):
        where_ = """
            pol.order_id = po.id 
            AND 
            pol.product_id = pr.id 
            AND 
            pr.product_tmpl_id = prtmpl.id 
            AND 
            po.picking_type_id = stpkt.id 
            AND
            pol.product_id IS NOT NULL
            %s
        """ % where_clause
        return where_

    def _group_by_sale(self, groupby=''):
        groupby_ = """
            sol.id,
            so.user_id, 
            date, 
            so.name, 
            so.warehouse_id, 
            so.partner_id, 
            sol.product_id, 
            product_name,
            product_uom_qty, 
            price_subtotal, 
            so.company_id, 
            prtmpl.licence_id, 
            nature, 
            sol.state
             %s
        """ % groupby
        return groupby_

    def _group_by_purchase(self, groupby=''):
        groupby_ = """
            pol.id,
            po.user_id, 
            date, 
            po.name, 
            stpkt.warehouse_id, 
            po.partner_id, 
            pol.product_id, 
            product_name,
            pol.product_uom_qty, 
            pol.price_subtotal, 
            po.company_id, 
            prtmpl.licence_id, 
            nature, 
            pol.state
             %s
        """ % groupby
        return groupby_

    def _query(self, with_clause='', fields=None, groupby='', from_clause='', fields_purchase=None, groupby_purchase='',
               from_clause_purchase=''):
        """
        :param with_clause:
        :param fields:
        :param groupby:
        :param from_clause:
        :param fields_purchase:
        :param groupby_purchase:
        :param from_clause_purchase:
        :return:
        """
        if not fields:
            fields = {}
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        return '%s (SELECT %s FROM %s WHERE %s GROUP BY %s UNION SELECT %s FROM %s WHERE %s GROUP BY %s)' % \
               (with_,
                self._select_sale(fields), self._from_sale(from_clause), self._where_sale(), self._group_by_sale(groupby),
                self._select_purchase(fields_purchase), self._from_purchase(from_clause_purchase), self._where_purchase(),
                self._group_by_purchase(groupby_purchase))

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))
