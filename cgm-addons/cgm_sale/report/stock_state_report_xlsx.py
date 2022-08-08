# -*- coding : UTF-8 -*-

import base64
import io

from odoo import models, _
from itertools import groupby


class StockStateReportXlsx(models.AbstractModel):
    _name = 'report.cgm_sale.cgm_report_stock_state_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Stock state XLSX'

    def _configure_workbook(self, workbook, sheet, order, order_lines):
        """
        Add headers (client, licence image, ...) for the workbook
        """
        # licence image
        if order.sale_order_template_id.licence_id.image_1920:
            output = io.BytesIO(base64.b64decode(order.sale_order_template_id.licence_id.image_1920))
            sheet.insert_image('D2', 'image', options={'image_data': output})

        style_highlight = workbook.add_format({'bold': True, 'pattern': 1, 'bg_color': '#E0E0E0', 'align': 'center'})

        bold_format = workbook.add_format({'bold': True})
        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'left'})
        # DATE
        sheet.write('A12', _('Date :'), style_highlight)
        if order.date_order:
            sheet.write('A13', order.date_order, date_format)
        # Expiration
        sheet.write('B12', _('Expiration :'), style_highlight)
        if order.validity_date:
            sheet.write('B13', order.validity_date, date_format)
        # Salesperson
        sheet.write('G12', _('Salesperson :'), style_highlight)
        if order.user_id:
            sheet.write('G13', order.user_id.name)
        sheet.write_blank('H12', '', style_highlight)

        headers = [_('SKU CODE'), _('DESCRIPTION'), _('THUMBNAIL'), _('EAN CODE'), _('QUANTITY'), _('QTY DESIRED'),
                   _('UNIT PRICE'), _('AMOUNT')]
        columns = ['A:A', 'B:B', 'C:C', 'D:D', 'E:E', 'F:F', 'G:G', 'H:H']
        col = 0
        row = 14

        for header in headers:
            sheet.write(row, col, header, style_highlight)
            col += 1

        for column in columns:
            sheet.set_column(column, 20)

    def write_sheet(self, workbook, sheet, order, order_lines):
        """
        Create the dynamic table
        """
        self._configure_workbook(workbook, sheet, order, order_lines)
        text_format_left = workbook.add_format({'valign': 'top'})
        text_format_right = workbook.add_format({'valign': 'top', 'align': 'right'})
        currency_format = workbook.add_format({'num_format': f'{order.currency_id.symbol} #.##0,0', 'valign': 'top'})
        qty_format = workbook.add_format({'num_format': '#.##0,0', 'valign': 'top'})
        col = 0
        row_begin = row = 15
        for ol in order_lines:
            if ol.product_id.default_code:
                sheet.write(row, col + 0, ol.product_id.default_code, text_format_left)
            sheet.write(row, col + 1, ol.product_id.name, text_format_left)
            if ol.product_id.image_128:
                output = io.BytesIO(base64.b64decode(ol.product_id.image_128))
                sheet.insert_image(row, col + 2, 'image', options={'image_data': output, 'x_offset': 10})
                sheet.set_row(row, 75)
            if ol.product_id.barcode:
                sheet.write(row, col + 3, ol.product_id.barcode, text_format_right)
            sheet.write_number(row, col + 4, ol.product_uom_qty, qty_format)
            sheet.write_number(row, col + 6, ol.price_unit, currency_format)
            sheet.write(row, col + 7, f'=F{row + 1}*G{row + 1}', currency_format)
            row += 1
        currency_sum_format = workbook.add_format(
            {'num_format': f'{order.currency_id.symbol} #.##0,0', 'bg_color': '#FFD8CE'})
        text_sum_format = workbook.add_format({'align': 'right', 'bg_color': '#FFD8CE'})
        sheet.write(row + 5, col + 6, _('Amount Total'), text_sum_format)
        sheet.write(row + 5, col + 7, f'=SUM(H{row_begin + 1}:H{row})', currency_sum_format)

    def generate_xlsx_report(self, workbook, data, so):
        for obj in so:
            order_line_ids = obj.order_line.filtered(lambda x: x.product_id.device_id)

            device_id_ol_ids = {}
            for ol_id in order_line_ids:
                device_id_ol_ids.setdefault(ol_id.product_id.device_id.id, []).append(ol_id)

            for key, order_lines in device_id_ol_ids.items():
                device_id = self.env['product.device'].browse(key)
                sheet = workbook.add_worksheet(device_id.name)
                self.write_sheet(workbook, sheet, obj, order_lines)
