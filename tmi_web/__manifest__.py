# -*- coding: utf-8 -*-
{
    'name': "Website Brand Logos", # DIUBAH
    'summary': """
        Display a dynamic list of brand logos on your website.""", # DIUBAH
    'description': """
        This module allows you to add brand logos or client images in the backend and display them on a dedicated website page.
    """,
    'author': "Programer Odoo 18 (Anda)",
    'website': "https://www.odoo.com",
    'category': 'Website/Website',
    'version': '18.0.1.0.0',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/brand_views.xml', # DIUBAH
        'views/client_views.xml', # DIUBAH
        'views/service_views.xml', # DIUBAH
        'views/product_views.xml', # DIUBAH
        'views/area_views.xml', # DIUBAH
        'views/menu_items.xml',
        'views/home_templates.xml', # DIUBAH
        'views/about_us_templates.xml', # DIUBAH
        'views/our_portofolio_templates.xml', # DIUBAH
        'views/our_product_templates.xml', # DIUBAH
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}