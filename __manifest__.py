# -*- coding: utf-8 -*-
{
    'name': 'Company Dynamic Header V2',
    'version': '0.1.0',
    'author': 'Benlever Pvt Ltd',
    'company': 'Benelever Pvt Ltd',
    'website': 'https://www.benlever.com',
    'maintainer': 'Benlever Pvt Ltd',
    'category': 'Accounting/Accounting',
    'sequence': 6,
    'summary': 'Allows you to set a custom logo for each journal type',
    'description': """
Allows you to set a custom logo for each journal type
""",
    'depends': ['sale','account'],
    'data': [
        'views/account_journal_views.xml',
        'views/report_invoice.xml',
        'views/bill_preview_template.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/res_users.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_custom_logo/static/src/xml/**/*',
            'pos_custom_logo/static/src/js/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
