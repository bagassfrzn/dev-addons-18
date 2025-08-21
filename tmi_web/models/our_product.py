from odoo import models, fields

class OurProduct(models.Model):
    _name = 'our.product'
    _description = 'our product'

    name = fields.Char('name')
    description = fields.Char('description')
    image = fields.Image('image')
    sequence = fields.Integer('Sequence')
    is_published = fields.Boolean('Is Published',default=True,copy=False)
    product_url = fields.Char('product Url')