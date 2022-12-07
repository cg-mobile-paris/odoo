# -*- coding: utf-8 -*-
{
    'name': 'ArkeUp Background Image',
    'summary': 'Change the Wallpaper Image of the Home Page',
    'description': 'This module allows to define the default wallpaper image of the home page.',
    'author': 'ArkeUp',
    'category': 'web',
    'license': 'LGPL-3',
    'version': '15.0.0.1',
    'depends': ['web_enterprise'],
    'data': [],
    'assets': {
        'web._assets_common_styles': [
            ('replace', 'web_enterprise/static/src/legacy/scss/ui.scss', 'arkeup_background_image/static/src/scss/ui.scss'),
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
