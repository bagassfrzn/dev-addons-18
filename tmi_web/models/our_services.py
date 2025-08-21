from odoo import models, fields

class OurServices(models.Model):
    _name = 'our.service'
    _description = 'our service'

    name = fields.Char('name')
    description = fields.Char('description')
    image = fields.Image('image')
    sequence = fields.Integer('Sequence')
    is_published = fields.Boolean('Is Published',default=True,copy=False)
    service_url = fields.Char('Service Url')