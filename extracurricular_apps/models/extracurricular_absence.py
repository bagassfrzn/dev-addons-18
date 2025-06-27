from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExtracurricularAbsence(models.Model):
    _name = 'extracurricular.absence'
    _description = 'Absensi Ekskul'

    name = fields.Char(string="Name", readonly=True, copy=False, default="Extracurricular absence")
    date = fields.Date(string="Tanggal", required=True, default=fields.Date.context_today)
    extracurricular_id = fields.Many2one('res.extracurricular', string="Ekskul", required=True)
    documentation = fields.Image(string="Dokumentasi (Foto)")
    absence_line_ids = fields.One2many('extracurricular.absence.line', 'absence_id', string="Data Absensi")
    documentation_place = fields.Char(string="Tempat Dokumentasi", default="Ruang Kelas")


    # Audit Fields
    create_uid = fields.Many2one('res.users', string='Dibuat oleh', readonly=True)
    create_date = fields.Datetime(string='Dibuat pada', readonly=True)
    write_uid = fields.Many2one('res.users', string='Diperbarui oleh', readonly=True)
    write_date = fields.Datetime(string='Diperbarui pada', readonly=True)

    # @api.onchange('extracurricular_id')
    # def _onchange_extracurricular_id(self):
    #     if self.extracurricular_id:
    #         students = self.extracurricular_id.member_ids.filtered(lambda s: s.extracurricular_contact_type == 'student')
    #         self.absence_line_ids = [(0, 0, {
    #             'partner_id': student.id,
    #         }) for student in students]

    @api.model
    def create(self, vals):
        extracurricular = self.env['res.extracurricular'].browse(vals.get('extracurricular_id'))

        # Cek apakah sequence_id ada
        if not extracurricular or not extracurricular.sequence_id:
            raise ValidationError(_("Ekstrakurikuler belum memiliki Sequence. Silakan atur Sequence terlebih dahulu."))

        # Generate name dari sequence
        vals['name'] = extracurricular.sequence_id.next_by_id()
        return super().create(vals)

class ExtracurricularAbsenceLine(models.Model):
    _name = 'extracurricular.absence.line'
    _description = 'Detail Absensi Ekskul'

    absence_id = fields.Many2one('extracurricular.absence', string="Absensi", required=True, ondelete='cascade')
    partner_id = fields.Many2one(
        'res.partner',
        string='Siswa',
        required=True,
        domain="[('extracurricular_contact_type','=','student'), ('extracurricular_ids', 'in', [parent.extracurricular_id])]"
    )

    status = fields.Selection([
        ('h', 'Hadir'),
        ('i', 'Izin'),
        ('s', 'Sakit'),
        ('a', 'Alpha')
    ], string='Status', required=True, default='h')
    notes = fields.Text(string='Catatan')

