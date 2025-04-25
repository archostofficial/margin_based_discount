# -*- coding: utf-8 -*-
{
    'name': 'Margin-Based Pricelist Discounts',
    'version': '1.0',
    'summary': 'Set minimum profit margins for pricelist discounts',
    'description': """
        This module extends Odoo's pricelist functionality to add margin-based limits on discounts.
        Features:
        - Set a minimum profit margin percentage over cost price
        - Automatically limit discounts to maintain the specified profit margin
        - Apply margin limits to individual pricelist items or all items in a pricelist
    """,
    'category': 'Sales/Sales',
    'author': 'ARC WEB',
    'website': 'https://arcweb.com.au',
    'depends': ['product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pricelist_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
