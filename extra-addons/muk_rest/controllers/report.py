import base64

from werkzeug import exceptions

from odoo import http
from odoo.http import request
from odoo.tools import misc, safe_eval

from odoo.addons.muk_rest import tools, core
from odoo.addons.muk_rest.tools.http import build_route


class ReportController(http.Controller):
    
    #----------------------------------------------------------
    # Components
    #----------------------------------------------------------
    
    @property
    def API_DOCS_COMPONENTS(self):
        return {
            'schemas': {
                'ReportList': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                            },
                            'model': {
                                'type': 'string',
                            },
                            'name': {
                                'type': 'string',
                            },
                            'report_name': {
                                'type': 'string',
                            },
                        },
                    },
                    'description': 'A list of reports.'
                },
                'ReportContent': {
                    'type': 'object',
                    'properties': {
                        'content': {
                            'type': 'string',
                        },
                        'report': {
                            'type': 'string',
                        },
                        'content_length': {
                            'type': 'integer',
                        },
                        'content_type': {
                            'type': 'string',
                        },
                        'type': {
                            'type': 'string',
                        },
                    },
                    'description': 'The report content.'
                },
            }
        }

    @core.http.rest_route(
        routes=build_route([
            '/reports',
            '/reports/<string:name>',
            '/reports/<string:name>/<string:model>',
        ]), 
        methods=['GET'],
        protected=True,
        docs=dict(
            tags=['Report'], 
            summary='Reports List', 
            description='Returns a list of reports based on the search criteria.',
            parameter={
                'name': {
                    'name': 'name',
                    'description': 'Report Name',
                    'schema': {
                        'type': 'string'
                    },
                },
                'model': {
                    'name': 'model',
                    'description': 'Model',
                    'schema': {
                        'type': 'string'
                    },
                },
            },
            responses={
                '200': {
                    'description': 'List of Reports', 
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/ReportList',
                            },
                            'example': [{
                                'id': 241,
                                'model': 'res.company',
                                'name': 'Hash integrity result PDF',
                                'report_name': 'account.report_hash_integrity'
                              }]
                        }
                    }
                }
            },
            default_responses=['400', '401', '500'],
        ),
    )
    def reports(self, name=None, model=None, **kw):
        domain = []
        if name:
            domain.append(['name', 'ilike', name])
        if model:
            domain.append(['model', '=', model])
    
        result = request.env['ir.actions.report'].search_read(
            domain, ['name', 'model', 'report_name']
        )
        return request.make_json_response(result)

    @core.http.rest_route(
        routes=build_route([
            '/report',
            '/report/<string:report>',
            '/report/<string:report>/<string:type>',
        ]), 
        methods=['GET'],
        protected=True,
        docs=dict(
            tags=['Report'], 
            summary='Report Download', 
            description='Returns the report.',
            parameter={
                'report': {
                    'name': 'report',
                    'description': 'Report',
                    'required': True,
                    'schema': {
                        'type': 'string'
                    },
                    'example': 'sale.report_saleorder',
                },
                'ids': {
                    'name': 'ids',
                    'description': 'Record IDs',
                    'required': True,
                    'schema': {
                        'type': 'string'
                    },
                    'example': '[1,2,3]',
                },
                'type': {
                    'name': 'type',
                    'description': 'Type',
                    'schema': {
                        'type': 'string'
                    }
                },
                'options': {
                    'name': 'options',
                    'description': 'Options',
                    'schema': {
                        'type': 'string'
                    },
                    'example': '{}',
                },
                'file_response': {
                    'name': 'file_response',
                    'description': 'Return the Report as a File',
                    'schema': {
                        'type': 'boolean'
                    }
                },
            },
            responses={
                '200': {
                    'description': 'List of Reports', 
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/ReportContent'
                            },
                            'example': {
                                'content': 'JVBERi0xLg==',
                                'content_length': 64,
                                'content_type': 'application/pdf',
                                'report': 'sale.report_saleorder',
                                'type': 'PDF'
                            }
                        },
                        'application/pdf': {
                            'schema': {
                                'type': 'string',
                                'format': 'binary'
                            }
                        },
                        'text/plain': {
                            'schema': {
                                'type': 'string',
                                'format': 'binary'
                            }
                        },
                        'text/html': {
                            'schema': {
                                'type': 'string',
                                'format': 'binary'
                            }
                        },
                        
                    }
                }
            },
            default_responses=['400', '401', '500'],
        ),
    )
    def report(self, report, ids, type='PDF', options=None, file_response=False, **kw):
        options = tools.common.parse_value(options, {})
        ids = tools.common.parse_value(ids, [])
        
        report_model = request.env['ir.actions.report']
        report_record = report_model._get_report_from_name(report)
        data, content_type, filename_extension = None, None, None
        
        if type.lower() == 'html':
            filename_extension = 'html'
            content_type = 'text/html'
            data = report_record._render_qweb_html(
                report, ids, data=options
            )[0]
        elif type.lower() == 'pdf':
            filename_extension = 'pdf'
            content_type = 'application/pdf'
            data = report_record._render_qweb_pdf(
                report, ids, data=options
            )[0]
        elif type.lower() == 'text':
            filename_extension = 'txt'
            content_type = 'text/plain'
            data = report_record._render_qweb_text(
                report, ids, data=options
            )[0]
        else:
            raise exceptions.BadRequest('Invalid Report Type!')
        
        if file_response and misc.str2bool(file_response):
            filename = '{}.{}'.format(report, filename_extension)
            if ids:
                records = request.env[report_record.model].browse(ids)
                if report_record.print_report_name and not len(records) > 1:
                    report_name = safe_eval.safe_eval(report_record.print_report_name, {
                        'object': records, 'time': safe_eval.time
                    })
                    filename = '{}.{}'.format(report_name, filename_extension)
            headers = [
                ('Content-Type', content_type),
                ('Content-Length',  len(data)),
                ('Content-Disposition', http.content_disposition(filename)),
            ]
            return request.make_response(data, headers)
        return request.make_json_response({
            'content': base64.b64encode(data),
            'content_type': content_type,
            'content_length': len(data),
            'report': report, 
            'type': type
        })
        