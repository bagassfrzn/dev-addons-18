from odoo import models, fields

class ImageBrand(models.Model):
    _name = 'image.brand'
    _description = 'image brand'

    name = fields.Char('Brand Name', required=True)
    image = fields.Image('Image',required=True, max_width=1920, max_height=1920)
    sequence = fields.Integer('Sequence')
    is_published = fields.Boolean('Is Published',default=True,copy=False)
    brand_url = fields.Char('Brand Url')

    