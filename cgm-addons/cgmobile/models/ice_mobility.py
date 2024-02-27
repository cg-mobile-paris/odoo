# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError
import requests
import logging
_logger = logging.getLogger(__name__)

COUNTRY_CODE_MAP = {
        "AF":	"AFG",
        "AL":	"ALB",
        "DZ":	"DZA",
        "AS":	"ASM",
        "AD":	"AND",
        "AO":	"AGO",
        "AI":	"AIA",
        "AQ":	"ATA",
        "AG":	"ATG",
        "AR":	"ARG",
        "AM":	"ARM",
        "AW":	"ABW",
        "AU":	"AUS",
        "AT":	"AUT",
        "AZ":	"AZE",
        "BS":	"BHS",
        "BH":	"BHR",
        "BD":	"BGD",
        "BB":	"BRB",
        "BY":	"BLR",
        "BE":	"BEL",
        "BZ":	"BLZ",
        "BJ":	"BEN",
        "BM":	"BMU",
        "BT":	"BTN",
        "BO":	"BOL",
        "BQ":	"BES",
        "BA":	"BIH",
        "BW":	"BWA",
        "BV":	"BVT",
        "BR":	"BRA",
        "IO":	"IOT",
        "BN":	"BRN",
        "BG":	"BGR",
        "BF":	"BFA",
        "BI":	"BDI",
        "CV":	"CPV",
        "KH":	"KHM",
        "CM":	"CMR",
        "CA":	"CAN",
        "KY":	"CYM",
        "CF":	"CAF",
        "TD":	"TCD",
        "CL":	"CHL",
        "CN":	"CHN",
        "CX":	"CXR",
        "CC":	"CCK",
        "CO":	"COL",
        "KM":	"COM",
        "CD":	"COD",
        "CG":	"COG",
        "CK":	"COK",
        "CR":	"CRI",
        "HR":	"HRV",
        "CU":	"CUB",
        "CW":	"CUW",
        "CY":	"CYP",
        "CZ":	"CZE",
        "CI":	"CIV",
        "DK":	"DNK",
        "DJ":	"DJI",
        "DM":	"DMA",
        "DO":	"DOM",
        "EC":	"ECU",
        "EG":	"EGY",
        "SV":	"SLV",
        "GQ":	"GNQ",
        "ER":	"ERI",
        "EE":	"EST",
        "SZ":	"SWZ",
        "ET":	"ETH",
        "FK":	"FLK",
        "FO":	"FRO",
        "FJ":	"FJI",
        "FI":	"FIN",
        "FR":	"FRA",
        "GF":	"GUF",
        "PF":	"PYF",
        "TF":	"ATF",
        "GA":	"GAB",
        "GM":	"GMB",
        "GE":	"GEO",
        "DE":	"DEU",
        "GH":	"GHA",
        "GI":	"GIB",
        "GR":	"GRC",
        "GL":	"GRL",
        "GD":	"GRD",
        "GP":	"GLP",
        "GU":	"GUM",
        "GT":	"GTM",
        "GG":	"GGY",
        "GN":	"GIN",
        "GW":	"GNB",
        "GY":	"GUY",
        "HT":	"HTI",
        "HM":	"HMD",
        "VA":	"VAT",
        "HN":	"HND",
        "HK":	"HKG",
        "HU":	"HUN",
        "IS":	"ISL",
        "IN":	"IND",
        "ID":	"IDN",
        "IR":	"IRN",
        "IQ":	"IRQ",
        "IE":	"IRL",
        "IM":	"IMN",
        "IL":	"ISR",
        "IT":	"ITA",
        "JM":	"JAM",
        "JP":	"JPN",
        "JE":	"JEY",
        "JO":	"JOR",
        "KZ":	"KAZ",
        "KE":	"KEN",
        "KI":	"KIR",
        "KP":	"PRK",
        "KR":	"KOR",
        "KW":	"KWT",
        "KG":	"KGZ",
        "LA":	"LAO",
        "LV":	"LVA",
        "LB":	"LBN",
        "LS":	"LSO",
        "LR":	"LBR",
        "LY":	"LBY",
        "LI":	"LIE",
        "LT":	"LTU",
        "LU":	"LUX",
        "MO":	"MAC",
        "MG":	"MDG",
        "MW":	"MWI",
        "MY":	"MYS",
        "MV":	"MDV",
        "ML":	"MLI",
        "MT":	"MLT",
        "MH":	"MHL",
        "MQ":	"MTQ",
        "MR":	"MRT",
        "MU":	"MUS",
        "YT":	"MYT",
        "MX":	"MEX",
        "FM":	"FSM",
        "MD":	"MDA",
        "MC":	"MCO",
        "MN":	"MNG",
        "ME":	"MNE",
        "MS":	"MSR",
        "MA":	"MAR",
        "MZ":	"MOZ",
        "MM":	"MMR",
        "NA":	"NAM",
        "NR":	"NRU",
        "NP":	"NPL",
        "NL":	"NLD",
        "NC":	"NCL",
        "NZ":	"NZL",
        "NI":	"NIC",
        "NE":	"NER",
        "NG":	"NGA",
        "NU":	"NIU",
        "NF":	"NFK",
        "MP":	"MNP",
        "NO":	"NOR",
        "OM":	"OMN",
        "PK":	"PAK",
        "PW":	"PLW",
        "PS":	"PSE",
        "PA":	"PAN",
        "PG":	"PNG",
        "PY":	"PRY",
        "PE":	"PER",
        "PH":	"PHL",
        "PN":	"PCN",
        "PL":	"POL",
        "PT":	"PRT",
        "PR":	"PRI",
        "QA":	"QAT",
        "MK":	"MKD",
        "RO":	"ROU",
        "RU":	"RUS",
        "RW":	"RWA",
        "RE":	"REU",
        "BL":	"BLM",
        "SH":	"SHN",
        "KN":	"KNA",
        "LC":	"LCA",
        "MF":	"MAF",
        "PM":	"SPM",
        "VC":	"VCT",
        "WS":	"WSM",
        "SM":	"SMR",
        "ST":	"STP",
        "SA":	"SAU",
        "SN":	"SEN",
        "RS":	"SRB",
        "SC":	"SYC",
        "SL":	"SLE",
        "SG":	"SGP",
        "SX":	"SXM",
        "SK":	"SVK",
        "SI":	"SVN",
        "SB":	"SLB",
        "SO":	"SOM",
        "ZA":	"ZAF",
        "GS":	"SGS",
        "SS":	"SSD",
        "ES":	"ESP",
        "LK":	"LKA",
        "SD":	"SDN",
        "SR":	"SUR",
        "SJ":	"SJM",
        "SE":	"SWE",
        "CH":	"CHE",
        "SY":	"SYR",
        "TW":	"TWN",
        "TJ":	"TJK",
        "TZ":	"TZA",
        "TH":	"THA",
        "TL":	"TLS",
        "TG":	"TGO",
        "TK":	"TKL",
        "TO":	"TON",
        "TT":	"TTO",
        "TN":	"TUN",
        "TR":	"TUR",
        "TM":	"TKM",
        "TC":	"TCA",
        "TV":	"TUV",
        "UG":	"UGA",
        "UA":	"UKR",
        "AE":	"ARE",
        "GB":	"GBR",
        "UM":	"UMI",
        "US":	"USA",
        "UY":	"URY",
        "UZ":	"UZB",
        "VU":	"VUT",
        "VE":	"VEN",
        "VN":	"VNM",
        "VG":	"VGB",
        "VI":	"VIR",
        "WF":	"WLF",
        "EH":	"ESH",
        "YE":	"YEM",
        "ZM":	"ZMB",
        "ZW":	"ZWE",
        "AX":	"ALA"
    }

class CountryState(models.Model):
    _inherit = 'res.country.state'

    ice_mobility_code = fields.Char(string='ICE Mobility Code', help='ICE Mobility Code')


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    ice_mobility_warehouse = fields.Boolean(string="Ice Mobility Warehouse")

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    ice_mobility_picking_type = fields.Boolean(string="Export to Ice Mobility")

class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    ice_mobility_delivery_mode = fields.Char(string='ICE Mobility Delivery Mode', help='ICE Mobility Delivery Mode')

class ProductProduct(models.Model):
    _inherit = "product.product"

    ice_mobility_code = fields.Char(string='Ice Mobility Code')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    ice_mobility_picking = fields.Boolean(string="Ice Mobility Picking", compute='_compute_ice_mobility_picking', compute_sudo=True)
    ice_mobility_export_date = fields.Datetime(string='ICE Mobility Sync Date', readonly=False)
    ice_mobility_export_number = fields.Char(string='ICE Mobility Sync Number', readonly=False)

    def _compute_ice_mobility_picking(self):
        icemo_picking_ids = self.filtered(lambda p: p.picking_type_id.ice_mobility_picking_type == True and p.picking_type_id.warehouse_id.ice_mobility_warehouse == True and p.location_dest_id.usage in ['customer', 'internal', 'supplier'])
        other_picking_ids = self - icemo_picking_ids
        icemo_picking_ids.update({'ice_mobility_picking': True})
        other_picking_ids.update({'ice_mobility_picking': False}) 

    def ice_mobility_scheduler_export(self):
        domain = [
                ('picking_type_id.warehouse_id.ice_mobility_warehouse', '=', True),
                ('state', 'in', ['assigned', 'confirmed', 'waiting']),
                ('picking_type_id.ice_mobility_picking_type', '=', True),
                ('location_dest_id.usage', 'in', ['customer', 'internal', 'supplier']),
                ('ice_mobility_export_date', '=', False),
        ]
        picking_ids = self.sudo().search(domain)
        picking_ids.sudo().ice_mobility_export()

    def ice_mobility_export(self):
        for picking in self:
            if picking.state in ['assigned', 'confirmed'] and picking.picking_type_id.ice_mobility_picking_type == True and picking.location_dest_id.usage in ['customer', 'internal', 'supplier']:
                try:
                    export_number = picking._ice_mobiliy_export()
                    picking.write({
                        'ice_mobility_export_date': datetime.now(),
                        'ice_mobility_export_number': export_number
                    })
                    log_message = "ICE Mobility Export: Picking %s exported with number %s" % (picking.name, export_number)
                    picking.message_post(body=log_message)
                    if picking.sale_id:
                        picking.sale_id.message_post(body=log_message)
                except Exception as e:
                    log_message = 'ICE Mobility Export Error: ' + str(e)
                    # create an activity
                    if not picking.activity_ids.filtered(lambda a: a.summary == log_message):
                        # picking.message_post(body=log_message)
                        if picking.sale_id:
                            picking.sale_id.message_post(body=log_message)
                        picking.activity_schedule(
                            'mail.mail_activity_data_warning',
                            summary=log_message,
                            user_id=self.env.user.id
                        )
                    continue
                self.env.cr.commit()

    def _ice_mobiliy_export(self):
        self.ensure_one()

        # get customer account from odoo params
        customer_account = self.env['ir.config_parameter'].get_param('cgmobile.ice_mobility_customer_account')
        if not customer_account:
            raise UserError('No customer account configured in odoo params. Key: cgmobile.ice_mobility_customer_account')

        # get default delivery mode from odoo params
        default_delivery_mode = self.env['ir.config_parameter'].get_param('cgmobile.ice_mobility_default_delivery_mode')
        if not default_delivery_mode:
            raise UserError('No default delivery mode configured in odoo params. Key: cgmobile.ice_mobility_default_delivery_mode')

        # get api endpoint from odoo params
        api_endpoint = self.env['ir.config_parameter'].get_param('cgmobile.ice_mobility_api_endpoint')
        if not api_endpoint:
            raise UserError('No api endpoint configured in odoo params. Key: cgmobile.ice_mobility_api_endpoint')

        # get basic auth username and password from odoo params
        basic_auth_username = self.env['ir.config_parameter'].get_param('cgmobile.ice_mobility_basic_auth_username')
        if not basic_auth_username:
            raise UserError('No basic auth username configured in odoo params. Key: cgmobile.ice_mobility_basic_auth_username')
        basic_auth_password = self.env['ir.config_parameter'].get_param('cgmobile.ice_mobility_basic_auth_password')
        if not basic_auth_password:
            raise UserError('No basic auth password configured in odoo params. Key: cgmobile.ice_mobility_basic_auth_password')

        sol_vals = []
        for move in self.move_lines:
            sol_vals.append({
                "ItemId": move.product_id.ice_mobility_code or "CGM-%s" % move.product_id.default_code,
                "SalesLineReference": move.id,
                "SalesPrice": move.sale_line_id.price_unit or 0,
                "SalesQty": move.product_uom_qty,
                "SalesUnit": "Pcs"
            })

        order_date = self.sale_id.date_order or self.create_date

        # check country code
        if not self.partner_id.country_id.code:
            raise UserError('Country code not found for partner %s' % self.partner_id.name)
        if self.partner_id.country_id.code not in COUNTRY_CODE_MAP:
            raise UserError('Country code %s not supported' % self.partner_id.country_id.code)

        so_vals = {
            "CustomerAccount": customer_account,
            "CustomerOrderDate": order_date.strftime('%Y-%m-%d %H:%M:%S'),
            "CustomerReference": self.sale_id.name or self.origin or self.name,
            "CustomerReference1": self.name,
            "CustomerReference2": str(self.id),
            "DeliveryAddress": {
                "City": self.partner_id.city,
                "Country": COUNTRY_CODE_MAP[self.partner_id.country_id.code],
                "LocationName": self.partner_id.name,
                "State": self.partner_id.state_id.ice_mobility_code,
                "Street": self.partner_id.street if not self.partner_id.street2 else '%s, %s' % (self.partner_id.street, self.partner_id.street2),
                "ZipCode": self.partner_id.zip,
            },
            "DeliveryMode": self.carrier_id.ice_mobility_delivery_mode or default_delivery_mode,
            "DeliveryTerms": "SC",
            "SalesLines": sol_vals,
            "Site": "ICE",
            "Warehouse": "ZAM"
        }

        # Make request to ICE Mobility API
        headers = {
            'Content-Type': 'application/json'
        }
        _logger.info('ICE Mobility Export: %s' % json.dumps(so_vals))
        response = requests.post(api_endpoint, data=json.dumps(so_vals), headers=headers, auth=(basic_auth_username, basic_auth_password))
        if response.status_code != 200:
            _logger.error('ICE Mobility Export Error: %s' % response.text)
            raise UserError('ICE Mobility API returned error: %s' % response.text)
        json_response = response.json()
        if json_response['Type'] == 'error':
            _logger.error('ICE Mobility Export Error: %s' % json_response['Message'])
            raise UserError('ICE Mobility API returned error: %s' % json_response['Message'])
        else:
            _logger.info('ICE Mobility Export Success: %s' % json_response['Data'])
            # return date from the response
            return json_response['Data']
        
    def send_to_shipper(self):
        """
        If no_send_to_shipper = True passed in Context then we can not call send shipment from carrier
        """
        context = dict(self._context)
        if context.get('no_send_to_shipper', False):
            return True
        return super(StockPicking, self).send_to_shipper()

    def set_quantities_done(self, quantities):
        """
        It takes a list of dictionaries, each dictionary containing a product_id and a quantity, and
        sets the quantity_done of the move_line_ids of the picking to the quantity in the dictionary
        
        :param quantities: [{'product_sku': 1, 'quantity': 1.0}, {'product_sku': 2, 'quantity': 1.0}]
        """
        self.ensure_one()
        # group quantities by product_sku
        skus = set([q['product_sku'] for q in quantities])
        # for each product_sku, sum the quantities
        quantities = [{'product_sku': sku, 'quantity': sum([q['quantity'] for q in quantities if q['product_sku'] == sku])} for sku in skus]
        # loop on quantities
        for quantity in quantities:
            # search stock move lines (detailled operations)
            mls = self.sudo().move_line_ids.filtered(lambda ml: ml.product_id.default_code == quantity['product_sku'])
            if not mls:
                # search on stock move (operations)
                moves = self.sudo().move_lines.filtered(lambda m: m.product_id.default_code == quantity['product_sku'])
                if not moves:
                    continue
                # set quantity done on stock move
                # taking into account the quantity demanded on the stock move
                for move in moves:
                    # if move is the last one, set the quantity to the remaining quantity
                    if move == moves[-1]:
                        qty_to_done = quantity['quantity']
                    else:
                        qty_to_done = min(move.product_uom_qty, quantity['quantity'])
                    move._set_quantity_done(qty_to_done)
                    quantity['quantity'] -= qty_to_done
                    if quantity['quantity'] <= 0:
                        break
            else:
                # set quantity done on stock move lines
                # taking into account the quantity demanded on the stock move
                for ml in mls:
                    # if ml is the last one, set the quantity to the remaining quantity
                    if ml == mls[-1]:
                        ml.qty_done = quantity['quantity']
                    else:
                        ml.qty_done = min(ml.product_uom_qty, quantity['quantity'])
                    quantity['quantity'] -= ml.qty_done
                    if quantity['quantity'] <= 0:
                        break


    def set_fullfiled(self, quantities, tracking_number, carrier_name=None):
        """
        It sets the quantities done for the picking and sets the carrier tracking ref and shippo
        delivery provider
        
        :param quantities: [{'product_sku': 1, 'quantity': 1.0}, {'product_sku': 2, 'quantity': 1.0}]
        :param tracking_number: The tracking number of the shipment
        :param carrier_name: The name of the carrier that you want to use
        """
        _logger.info('set_fullfiled: {"quantities": %s, "tracking_number": "%s", "carrier_name": "%s"}' % (str(quantities), tracking_number, carrier_name))
        try:
            self.ensure_one()
            self.set_quantities_done(quantities)
            carrier_id = self.env['delivery.carrier'].search([('name', '=', self.env.user.name)], limit=1)
            if not carrier_id:
                carrier_id = self.env['delivery.carrier'].sudo().create({
                    'name': self.env.user.name,
                    'delivery_type': 'fixed',
                    'product_id': self.env['product.product'].search([('name', 'ilike', 'Shipping'), ('type', '=', 'service')], limit=1).id,
                })
            self.write({
                'carrier_id': carrier_id.id,
                'carrier_tracking_ref': tracking_number,
                'shippo_delivery_provider': carrier_name,
            })
            self.message_post(body="""
            <p>
                Set as Fulfilled.
                <ul>
                    <li>Shipping Method: %s</li>
                    <li>Tracking number: %s</li>
                    <li>Carrier: %s</li>
                    <li>Products: %s</li>
                </ul>
            </p>
            """ % (carrier_id.name, tracking_number, carrier_name, quantities))
            if 'sale_id' in self and self.sale_id:
                self.sale_id.message_post(body="""
                <p>
                    Transfer <b>%s</b> set as Fulfilled.
                    <ul>
                        <li>Shipping Method: %s</li>
                        <li>Tracking number: %s</li>
                        <li>Carrier: %s</li>
                        <li>Products: %s</li>
                    </ul>
                </p>
                """ % (self.name, carrier_id.name, tracking_number, carrier_name, quantities))
            self.with_context({'skip_immediate': True, 'skip_backorder': True, 'no_send_to_shipper': True}).button_validate()
            return True
        except Exception as e:
            mail_activity_obj = self.env['mail.activity'].sudo()
            model_id = self.env["ir.model"].sudo().search([("model", "=", "stock.picking")])
            warning_id = self.env.ref('mail.mail_activity_data_warning')
            note = """
                    <p>
                        ERROR - Transfer <b>%s</b> set as Fulfilled : <p>%s</p>
                        <ul>
                            <li>Tracking number: %s</li>
                            <li>Carrier: %s</li>
                            <li>Products: %s</li>
                        </ul>
                    </p>
                    """ % (self.name, str(e), tracking_number, carrier_name, quantities)
            mail_activity_obj.create({
                'summary':'Issue when fulfilled',
                'note': note,
                'date_deadline': datetime.now(),
                'user_id': 2,
                'res_id': self.id,
                'res_model_id': model_id.id,
                'activity_type_id': warning_id.id})
            raise e
