from odoo import models, fields

class OurArea(models.Model):
    _name = 'our.area'
    _description = 'our area'

    name = fields.Char('name')
    description = fields.Char('description')
    area_icon = fields.Image('image')
    sequence = fields.Integer('Sequence')
    is_published = fields.Boolean('Is Published',default=True,copy=False)
    area_url = fields.Char('area Url')