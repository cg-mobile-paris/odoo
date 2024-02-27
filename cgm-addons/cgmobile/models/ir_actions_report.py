# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def retrieve_attachment(self, record):
        # Override this method in order to force to re-render the pdf in case of
        # using snailmail
        if self.report_name == 'cgmobile.report_pdf_file'\
        and record.message_main_attachment_id\
        and (
            record.message_main_attachment_id.mimetype == 'application/pdf' or \
            record.message_main_attachment_id.mimetype.startswith('image')
        ):
            return record.message_main_attachment_id
        return super(IrActionsReport, self).retrieve_attachment(record)
