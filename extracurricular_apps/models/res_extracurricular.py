from odoo import models, fields, api

class ResExtracurricular(models.Model):
    _name = 'res.extracurricular'
    _description = 'res.extracurricular'

    name = fields.Char('Nama Ekskull',required=True)
    coach_id = fields.Many2one('res.partner', string='Pelatih',domain=[('extracurricular_contact_type','=','coach')])
    advisor_id = fields.Many2one('res.partner', string='Pembina',domain=[('extracurricular_contact_type','=','teacher')])
    lead_id = fields.Many2one('res.partner', string='Ketua',domain=[('extracurricular_contact_type','=','lead')])
    logo = fields.Image('logo')
    member_ids = fields.Many2many(
                                    'res.partner',
                                    'partner_extracurricular_rel',
                                    'partner_id',
                                    'extracurricular_id',
                                    string='Member')
    sequence_id = fields.Many2one(
        'ir.sequence',
        string='Sequence Absensi',
        help='Sequence yang akan digunakan untuk penomoran absensi pada ekskul ini.'
    )

    member_count = fields.Integer('member_count', compute="_compute_member_count",store=True)

    @api.depends('member_ids')
    def _compute_member_count(self):
        for record in self:
            # record.member_count = len(record.member_ids)
            students = record.member_ids.filtered(lambda p: p.extracurricular_contact_type == 'student')
            record.member_count = len(students)

    def action_view_member(self):
        self.ensure_one()
        # print(f"Anggota Ekskul ID: {self.id}")
        # print(f"Anggota terkait: {[p.name for p in self.member_ids]}")
        return{
            'type':'ir.actions.act_window',
            'name':'Member',
            'view_mode':'list,form',
            'res_model':'res.partner',
            'domain':[('id','in',self.member_ids.ids),('extracurricular_contact_type','=','student')],
            'context':dict(self.env.context,default_extracurricular_ids=[self.id])
        }

    

