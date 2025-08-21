from odoo import models, fields

class ImageBrand(models.Model):
    _name = 'our.client'
    _description = 'our client'

    name = fields.Char('Brand Name', required=True)
    image = fields.Image('Image',required=True, max_width=1920, max_height=1920)
    sequence = fields.Integer('Sequence')
    is_published = fields.Boolean('Is Published',default=True,copy=False)
    client_url = fields.Char('Brand Url')
    description = fields.Char('Description')
    category = fields.Selection([
        ('shipowner', 'Shipowner & Management'),
        ('factories', 'Factories / Plantation'),
        ('service', 'Service Provider')
    ], string='Category', required=True, default="shipowner")
    