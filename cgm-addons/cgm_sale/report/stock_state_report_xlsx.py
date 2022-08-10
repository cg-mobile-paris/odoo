# -*- coding : UTF-8 -*-

import base64
import io

from odoo import models, _
from itertools import groupby


class StockStateReportXLSX(models.AbstractModel):
    _name = 'report.cgm_sale.cgm_report_stock_state_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Stock state XLSX'

    @staticmethod
    def _configure_workbook(workbook, sheet, order):
        """
        Add headers (client, licence image, ...) for the workbook
        :param workbook:
        :param sheet:
        :param order:
        :return:
        """
        # licence image
        if order.sale_order_template_id.licence_id.image_1920:
            output = io.BytesIO(base64.b64decode(order.sale_order_template_id.licence_id.image_1920))
            sheet.insert_image('D2', 'image', options={'image_data': output})

        style_highlight_left = workbook.add_format({'bold': True, 'pattern': 1, 'bg_color': '#E0E0E0', 'align': 'left', 'font_size': 13})
        style_highlight_center = workbook.add_format({'bold': True, 'pattern': 1, 'bg_color': '#E0E0E0',
                                                      'align': 'center', 'font_size': 13})
        text_format = workbook.add_format({'font_size': 13})
        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'left', 'font_size': 13})
        # DATE
        sheet.write('A12', _('Date'), style_highlight_left)
        if order.date_order:
            sheet.write('A13', order.date_order, date_format)
        # Expiration
        sheet.write('B12', _('Expiration'), style_highlight_left)
        if order.validity_date:
            sheet.write('B13', order.validity_date, date_format)
        # Salesperson
        sheet.write('G12', _('Salesperson'), style_highlight_left)
        if order.user_id:
            sheet.write('G13', order.user_id.name, text_format)
        sheet.write_blank('H12', '', style_highlight_left)

        headers = [_('SKU CODE'), _('DESCRIPTION'), _('THUMBNAIL'), _('EAN CODE'), _('QUANTITY'), _('QTY DESIRED'),
                   _('UNIT PRICE'), _('AMOUNT')]
        columns = ['A:A', 'B:B', 'C:C', 'D:D', 'E:E', 'F:F', 'G:G', 'H:H']
        col = 0
        row = 14

        for header in headers:
            sheet.write(row, col, header, style_highlight_center)
            col += 1

        for column in columns:
            if column == 'B:B':
                sheet.set_column(column, 40)
                continue
            sheet.set_column(column, 20)

    @staticmethod
    def _write_sheet(workbook, sheet, order, order_lines):
        """
        Create the dynamic table
        :param workbook:
        :param sheet:
        :param order:
        :param order_lines:
        :return:
        """
        StockStateReportXLSX._configure_workbook(workbook, sheet, order)
        text_format_left = workbook.add_format({'valign': 'top', 'font_size': 13})
        text_format_right = workbook.add_format({'valign': 'top', 'align': 'right', 'font_size': 13})
        symbol = order.currency_id.symbol
        currency_format = workbook.add_format({'num_format': f'{symbol} #.##', 'valign': 'top', 'font_size': 13})
        qty_format = workbook.add_format({'num_format': '0', 'valign': 'top', 'font_size': 13})
        col = 0
        row_begin = row = 15
        for ol in order_lines:
            if ol.product_id.default_code:
                sheet.write(row, col + 0, ol.product_id.default_code, text_format_left)
            sheet.write(row, col + 1, ol.product_id.name, text_format_left)
            if ol.product_id.image_128:
                output = io.BytesIO(base64.b64decode(ol.product_id.image_128))
                sheet.insert_image(row, col + 2, 'image', options={'image_data': output, 'x_offset': 15, 'y_offset': 10})
                sheet.set_row(row, 120)
            if ol.product_id.barcode:
                sheet.write(row, col + 3, ol.product_id.barcode, text_format_right)
            sheet.write_number(row, col + 4, ol.product_uom_qty, qty_format)
            sheet.write_number(row, col + 5, 0.00, qty_format)
            sheet.write_number(row, col + 6, ol.price_unit, currency_format)
            sheet.write(row, col + 7, f'=F{row + 1}*G{row + 1}', currency_format)
            row += 1
        currency_sum_format = workbook.add_format({'num_format': f'{symbol} #.##', 'bg_color': '#FFD8CE', 'font_size': 13})
        text_sum_format = workbook.add_format({'align': 'right', 'bg_color': '#FFD8CE', 'font_size': 13})
        sheet.write(row + 5, col + 6, _('Amount Total'), text_sum_format)
        sheet.write(row + 5, col + 7, f'=SUM(H{row_begin + 1}:H{row})', currency_sum_format)

    def generate_xlsx_report(self, workbook, data, objs):
        """
        Generate xls report
        :param workbook:
        :param data:
        :param objs:
        :return:
        """
        for order in objs:
            device_summary = {}
            for line in order.order_line.filtered(lambda ol: not ol.display_type):
                device_summary.setdefault(line.product_id.device_id, []).append(line)
            if not device_summary:
                continue
            for device, lines in device_summary.items():
                sheet = workbook.add_worksheet(device and device.name or _('Indefinite'))
                StockStateReportXLSX._write_sheet(workbook, sheet, order, lines)
