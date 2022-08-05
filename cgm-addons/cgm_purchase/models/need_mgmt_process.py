# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class NeedMgmtProcess(models.Model):
    _name = 'need.mgmt.process'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Need Management Process'

    name = fields.Char(required=True)
    priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent')], 'Priority', default='0', index=True)
    reference = fields.Char('Reference', required=True)
    date = fields.Date('Date', required=False)
    date_approve = fields.Date('Date Approve', required=False)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True)
    licence_id = fields.Many2one('product.licence', 'Licence', required=False)
    state = fields.Selection([('draft', 'Draft'), ('checked', 'Checked'), ('sent', 'Sent'), ('confirmed', 'Confirmed'),
                              ('po_generated', 'PO Generated'), ('done', 'Done'), ('cancel', 'Cancel')], 'State', default='draft',
                             track_visibility='always')
    color = fields.Integer('Color', required=False, default=10)
    notes = fields.Html('Notes', required=False)
    company_id = fields.Many2one('res.company', 'Company', required=False)
    need_mgmt_process_line_ids = fields.One2many('need.mgmt.process.line', 'need_mgmt_process_id', 'Need Mgmt Process Lines')
    purchase_order_ids = fields.One2many('purchase.order', 'need_mgmt_process_id', 'Purchase Orders', required=False)
    po_count = fields.Integer('PO Count', compute='_compute_po_count', store=True)
    responsible_id = fields.Many2one('res.users', 'Responsible', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    category_ids = fields.Many2many('product.category', 'need_mgmt_process_product_category_rel', 'template_id', 'category_id',
                                    'Families', required=False)
    device_ids = fields.Many2many('product.device', 'need_mgmt_process_product_device_rel', 'template_id', 'device_id',
                                  'Devices', required=False)
    number_of_days = fields.Float('Number of Days', help='Period of validity of stock')

    @api.model
    def default_get(self, fields_list):
        res = super(NeedMgmtProcess, self).default_get(fields_list)
        if not res.get('reference') and 'reference' not in res:
            res.update({'reference': self.env['ir.sequence'].next_by_code('need.mgmt.process.seq')})
        if not res.get('date') and 'date' not in res:
            res.update({'date': fields.Date.today()})
        if not res.get('user_id') and 'user_id' not in res:
            res.update({'user_id': self.env.user.id})
        if not res.get('responsible_id') and 'responsible_id' not in res:
            res.update({'responsible_id': self.env.user.id})
        if not res.get('company_id') and 'company_id' not in res:
            res.update({'company_id': self.env.user.company_id.id})
        if not res.get('currency_id') and 'currency_id' not in res:
            res.update({'currency_id': self.env.ref('base.USD').id})
        return res

    @api.depends('purchase_order_ids')
    def _compute_po_count(self):
        for record in self:
            record.po_count = len(record.purchase_order_ids)

    @api.onchange('licence_id', 'category_ids', 'device_ids')
    def _onchange_licence_categories_devices(self):
        """
        Load products according to the selected licence
        :return: None
        """
        if not self.licence_id:
            return {}
        self.update({'need_mgmt_process_line_ids': [(6, 0, [])]})
        products = self.licence_id.product_ids
        if not products:
            return {}
        if self.category_ids:
            products = products.filtered(lambda p: p.categ_id.id in self.category_ids.ids)
        if self.device_ids:
            products = products.filtered(lambda p: p.device_id.id in self.device_ids.ids)
        device_summary = {}
        for product in products:
            device_summary.setdefault(product.device_id, []).append(product)
        need_mgmt_process_lines = []
        for device, products in device_summary.items():
            need_mgmt_process_lines.append((0, 0, {'display_type': 'line_section', 'name': device.name or _('Indefinite')}))
            for product in products:
                seller = product.seller_ids and product.seller_ids[0]
                need_mgmt_process_lines.append((0, 0, {'product_id': product.id,
                                                       'name': product.name,
                                                       'product_qty': 0.0,
                                                       'price_unit': seller and seller.price,
                                                       'seller_id': seller and seller.id}))
        self.update({'need_mgmt_process_line_ids': need_mgmt_process_lines})
        return {}

    def button_check_stock(self):
        """

        :return:
        """
        self.ensure_one()
        self.need_mgmt_process_line_ids.check_stock()
        self.write({'state': 'checked'})
        return True

    def button_send_by_mail(self):
        """

        :return:
        """
        self.ensure_one()
        self.write({'state': 'sent'})
        return True

    def button_print(self):
        """

        :return:
        """
        self.ensure_one()
        self.write({'state': 'sent'})
        return self.env.ref('cgm_purchase.action_report_need_mgmt_process').report_action(self)

    def button_confirm(self):
        """

        :return:
        """
        self.ensure_one()
        self.write({'state': 'confirmed', 'date_approve': fields.Date.today()})
        return True

    def button_generate_pos(self):
        """
        Generate all POs from lines grouped by seller
        :return:
        """
        self.ensure_one()
        partner_summary = {}
        po_obj = self.env['purchase.order']
        need_mgmt_process_lines = self.need_mgmt_process_line_ids.filtered(lambda nmpl: not nmpl.display_type and nmpl.product_qty > 0)
        if not need_mgmt_process_lines:
            raise ValidationError(_('There is no POs to generate.'))
        if any([not nmpl.seller_id for nmpl in need_mgmt_process_lines]):
            raise ValidationError(_('There is a line without Seller defined. \n'
                                    'Please fill Seller in lines for which a PO should be generated.'))
        for nmpl in need_mgmt_process_lines:
            partner_summary.setdefault(nmpl.seller_id.name, []).append(nmpl)
        for partner, nmpls in partner_summary.items():
            po_obj.create({
                'partner_id': partner.id,
                'order_line': [(0, 0, {
                    'product_id': nmpl.product_id.id,
                    'product_qty': nmpl.product_qty,
                    'price_unit': nmpl.price_unit}) for nmpl in nmpls],
                'need_mgmt_process_id': self.id,
                'currency_id': self.currency_id.id})
        self.write({'state': 'po_generated'})
        return True

    def button_validate(self):
        """

        :return:
        """
        self.ensure_one()
        self.write({'state': 'done'})
        return True

    def button_cancel(self):
        """

        :return:
        """
        self.purchase_order_ids.button_cancel()
        self.write({'state': 'cancel', 'date_approve': False})
        return True

    def button_draft(self):
        """

        :return:
        """
        self.write({'state': 'draft'})
        return True

    def button_view_pos(self):
        """

        :return:
        """
        self.ensure_one()
        action = self.env.ref('purchase.purchase_rfq', raise_if_not_found=False)
        if not action:
            return False
        action = action.read()[0]
        action['domain'] = [('id', 'in', self.purchase_order_ids.ids)]
        action['context'] = {'default_need_mgmt_process_id': self.id}
        return action

    def action_view_pos(self):
        """

        :return:
        """
        self.ensure_one()
        return self.button_view_pos()
