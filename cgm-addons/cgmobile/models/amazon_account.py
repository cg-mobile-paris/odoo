# -*- coding: utf-8 -*-

import re
from odoo import models
# from odoo.addons.sale_amazon.models import mws_connector as mwsc # FIXME lor v17: no available in v17
# from odoo.addons.sale_amazon_spapi import const, utils as amazon_utils # FIXME lor v14
from odoo.addons.sale_amazon import const, utils as amazon_utils # FIXME lor v17: redirection




class AmazonAccount(models.Model):
    _inherit = 'amazon.account'

    def _get_alternative_sku_patterns(self):
        """ Return a list of patterns to try to find alternative SKU """
        patterns = [(r'_FBA$', r''), (r'_FBA1$', r''), (r'_FBA-stickerless$', r''), (r'\.\d_FBA$', r''), (r'^New_(.+)_FBA$', r'\1'),(r'-FBA$', r''),(r'-stickerless$', r''),(r'.\d', r'')]
        others = self.env["ir.config_parameter"].sudo().get_param("cgmobile.alternative_sku_patterns", False)
        if others:
            try:
                patterns += eval(others)
            except:
                pass
        return patterns

    # def _get_offer(self, sku, marketplace):  # FIXME lor v14 replace by "def _find_or_create_offer(self, sku, marketplace):"
    #     """ Override to manage alternative FBA SKU """
    #     offer = super(AmazonAccount, self)._get_offer(sku, marketplace)
    #
    #     # If the offer has been linked with the default product, search if SKU is an alternative
    #     # patterns
    #     if 'sale_amazon.default_product' in offer.product_id._get_external_ids().get(offer.product_id.id, []):
    #         # for each pattern try to deduct the correct sku and check if exists
    #         for pattern, string in self._get_alternative_sku_patterns():
    #             primary_sku = re.sub(pattern, string, sku)
    #             product = self._get_product(primary_sku, None, None, None, fallback=False)
    #             if product:
    #                 offer.product_id = product.id
    #                 break
    #
    #     return offer

    def _find_or_create_offer(self, sku, marketplace):  # FIXME lor update for v17"
        """ Override to manage alternative FBA SKU """
        offer = super(AmazonAccount, self)._find_or_create_offer(sku, marketplace)

        # If the offer has been linked with the default product, search if SKU is an alternative
        # patterns
        if 'sale_amazon.default_product' in offer.product_id._get_external_ids().get(offer.product_id.id, []):
            # for each pattern try to deduct the correct sku and check if exists
            for pattern, string in self._get_alternative_sku_patterns():
                primary_sku = re.sub(pattern, string, sku)
                product = self._get_product(primary_sku, None, None, None, fallback=False)
                if product:
                    offer.product_id = product.id
                    break

        return offer

    # def _get_order(self, order_data, items_data, amazon_order_ref): # FIXME lor v17: don't find similar function
    #     """ Find or create a sale order based on Amazon data. """
    #     order, order_found, status = super(AmazonAccount, self)._get_order(order_data, items_data, amazon_order_ref)
    #
    #     # If order just created, check if we should change the invoice partner
    #     if not order_found:
    #         # find the marketplace
    #         marketplace = self.env['amazon.marketplace'].search([('api_ref', '=', order_data['MarketplaceId'])])
    #         if marketplace.invoice_partner_id:
    #             order.invoice_partner_id = marketplace.invoice_partner_id.id
    #
    #     return order, order_found, status
    
    def _create_order_from_data(self, order_data):  # FIXME V17; Ok
        """ Create a new sales order based on the provided order data.

        Note: self.ensure_one()

        :param dict order_data: The order data to create a sales order from.
        :return: The newly created sales order.
        :rtype: record of `sale.order`
        """
        order = super(AmazonAccount, self)._create_order_from_data(order_data)
        # If order just created, check if we should change the invoice partner
        marketplace = self.env['amazon.marketplace'].search([('api_ref', '=', order_data['MarketplaceId'])])
        if marketplace.fba_invoice_partner_id:
            order.partner_invoice_id = marketplace.fba_invoice_partner_id
        return order

    # def _process_order_lines(
    #         self, items_data, shipping_code, shipping_product, currency, fiscal_pos,
    #         marketplace_api_ref): # FIXME lor v17: don't find similar function
    #     """ Return a list of sale order line vals based on Amazon order items data. """
    #
    #     lines = super(AmazonAccount, self)._process_order_lines(items_data, shipping_code, shipping_product, currency, fiscal_pos, marketplace_api_ref)
    #
    #     for item_data in items_data:
    #         item_ref = mwsc.get_string_value(item_data, 'OrderItemId')
    #         quantity = mwsc.get_integer_value(item_data, 'QuantityOrdered')
    #         sales_price = mwsc.get_amount_value(item_data, 'ItemPrice')
    #         tax_amount = mwsc.get_amount_value(item_data, 'ItemTax')
    #         shipping_price = mwsc.get_amount_value(item_data, 'ShippingPrice')
    #         shipping_tax = mwsc.get_amount_value(item_data, 'ShippingTax')
    #
    #         marketplace = self.active_marketplace_ids.filtered(
    #             lambda m: m.api_ref == marketplace_api_ref)
    #
    #         if marketplace.do_not_import_tax:
    #             subtotal = sales_price - tax_amount if marketplace.tax_included else sales_price
    #
    #             # find the corresponding line from lines
    #             for line in lines:
    #                 if line['amazon_item_ref'] == item_ref:
    #                     # compare the subtotal
    #                     if line['price_unit'] * line['product_uom_qty'] != subtotal:
    #                         # remove taxes
    #                         line['price_unit'] = round(subtotal / quantity, 2)
    #                         line['tax_id'] = [(5, 0, 0)]
    #                 elif line['product_id'] == shipping_product.id:
    #                     # compare the shipping price
    #                     if line['price_unit'] != shipping_price:
    #                         # it seems that tax is different, we need to fix that
    #                         line['price_unit'] = shipping_price
    #                         line['tax_id'] = [(5, 0, 0)]
    #
    #     return lines
    
    def _prepare_order_lines_values(self, order_data, currency, fiscal_pos, shipping_product):
        # FIXME lor v17
        """ Prepare the values for the order lines to create based on Amazon data.

        Note: self.ensure_one()

        :param dict order_data: The order data related to the items data.
        :param record currency: The currency of the sales order, as a `res.currency` record.
        :param record fiscal_pos: The fiscal position of the sales order, as an
                                  `account.fiscal.position` record.
        :param record shipping_product: The shipping product matching the shipping code, as a
                                        `product.product` record.
        :return: The order lines values.
        :rtype: dict
        """
        lines = super(AmazonAccount, self)._prepare_order_lines_values(order_data, currency, fiscal_pos, shipping_product)

        def pull_items_data(amazon_order_ref_):
            """ Pull all items data for the order to synchronize.

            :param str amazon_order_ref_: The Amazon reference of the order to synchronize.
            :return: The items data.
            :rtype: list
            """
            items_data_ = []
            # Order items are pulled in batches. If more order items than those returned can be
            # synchronized, the request results are paginated and the next page holds another batch.
            has_next_page_ = True
            while has_next_page_:
                # Pull the next batch of order items.
                items_batch_data_, has_next_page_ = amazon_utils.pull_batch_data(
                    self, 'getOrderItems', {}, path_parameter=amazon_order_ref_
                )
                items_data_ += items_batch_data_['OrderItems']
            return items_data_
        
        amazon_order_ref = order_data['AmazonOrderId']
        marketplace_api_ref = order_data['MarketplaceId']
        items_data = pull_items_data(amazon_order_ref)

        for item_data in items_data:
            item_ref = item_data['OrderItemId']
            quantity = item_data['QuantityOrdered']
            sales_price = float(item_data.get('ItemPrice', {}).get('Amount', 0.0))
            tax_amount = float(item_data.get('ItemTax', {}).get('Amount', 0.0))
            shipping_price = float(item_data.get('ShippingPrice', {}).get('Amount', '0'))
            shipping_tax = float(item_data.get('ShippingTax', {}).get('Amount', '0'))

            marketplace = self.active_marketplace_ids.filtered(
                lambda m: m.api_ref == marketplace_api_ref)
            subtotal = sales_price - tax_amount if marketplace.tax_included else sales_price

            if marketplace.do_not_import_tax:
                subtotal = sales_price - tax_amount if marketplace.tax_included else sales_price

                # find the corresponding line from lines
                for line in lines:
                    if line['amazon_item_ref'] == item_ref:
                        # compare the subtotal
                        if line['price_unit'] * line['product_uom_qty'] != subtotal:
                            # remove taxes
                            line['price_unit'] = round(subtotal / quantity, 2)
                            line['tax_id'] = [(5, 0, 0)]
                    elif line['product_id'] == shipping_product.id:
                        # compare the shipping price
                        if shipping_price == 0:
                            line['tax_id'] = [(5, 0, 0)]
                        elif line['price_unit'] != shipping_price:
                            # it seems that tax is different, we need to fix that
                            line['price_unit'] = shipping_price
                            line['tax_id'] = [(5, 0, 0)]
        return lines