from odoo import models, fields

# This is a class that inherits from the base model.
class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string='Is Customer', compute='_compute_is_customer', compute_sudo=True, store=False, search='_search_is_customer')
    is_supplier = fields.Boolean(string='Is Vendor', compute='_compute_is_supplier', compute_sudo=True, store=False, search='_search_is_supplier')

    def _compute_is_customer(self):
        '''
        Compute the value of the field is_customer. This field is set to True if any Sales Order is linked to the partner
        '''
        for record in self:
            record.is_customer = 'Customer' in record.category_id.mapped('name') or self.env['sale.order'].search_count([('partner_id', '=', record.id)]) > 0

    def _search_is_customer(self, operator, value):
        '''
        Search function for the field is_customer. This field is set to True if any Sales Order is linked to the partner
        '''
        if (operator == '=' and value) or (operator == '!=' and not value):
            return ['|', ('sale_order_ids', '!=', False), ('category_id', '=', 'Customer')]
        elif (operator == '=' and not value) or (operator == '!=' and value):
            return ['&', ('sale_order_ids', '=', False), ('category_id', '!=', 'Customer')]
        return []

    def _compute_is_supplier(self):
        '''
        Compute the value of the field is_supplier. This field is set to True if any Purchase Order is linked to the partner
        '''
        for record in self:
            record.is_supplier = 'Supplier' in record.category_id.mapped('name') or self.env['purchase.order'].search_count([('partner_id', '=', record.id)]) > 0

    def _search_is_supplier(self, operator, value):
        '''
        Search function for the field is_supplier. This field is set to True if any Purchase Order is linked to the partner
        '''
        if (operator == '=' and value) or (operator == '!=' and not value):
            return ['|', ('id', 'in', self.env['purchase.order'].search([]).partner_id.ids), ('category_id', '=', 'Supplier')]
        elif (operator == '=' and not value) or (operator == '!=' and value):
            return ['&', ('id', 'not in', self.env['purchase.order'].search([]).partner_id.ids), ('category_id', '!=', 'Supplier')]
        return []