from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    extracurricular_ids = fields.Many2many(
                                            'res.extracurricular', #comodel
                                            'partner_extracurricular_rel', #tabel relation
                                            'extracurricular_id', #column 2 representasi dari id ekskulnya
                                            'partner_id', #column 1 representasi dari id contact
                                            string='Extracurricular')

    extracurricular_contact_type = fields.Selection([
        ('administrator', 'Administrator'),
        ('teacher', 'Teacher'),
        ('coach', 'Coach'),
        ('student', 'student')
    ], string='Contact type', required=True)

    extracurricular_contact_position = fields.Selection([
        ('leader','Leader'),
        ('member','Member')
    ],string='Position',required=True)

    grade = fields.Selection([
        ('X', 'X'),
        ('XI', 'XI'),
        ('XII', 'XII')
    ], string='Grade')

    major = fields.Selection([
        ('RPL', 'RPL'),
        ('BDP', 'BDP'),
        ('OTKP', 'OTKP'),
        ('AKL', 'AKL')
    ], string='major')



   
    