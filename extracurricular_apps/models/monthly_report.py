# models/monthly_report.py
from odoo import models, fields, _
from odoo.exceptions import ValidationError

class ExtracurricularMonthlyReport(models.Model):
    _name = 'extracurricular.monthly.report'
    _description = 'Laporan Bulanan Ekskul'
    _order = 'year desc, month desc, extracurricular_id'

    name = fields.Char(string="Nama Laporan", required=True, default="Monthly Report")
    extracurricular_id = fields.Many2one('res.extracurricular', string="Ekskul", required=True)
    month = fields.Selection(
        selection=[(str(i), f'{i:02}') for i in range(1, 13)],
        string='Bulan',
        required=True
    )
    year = fields.Integer(string="Tahun", required=True)
    report_line_ids = fields.One2many('extracurricular.monthly.report.line', 'report_id', string="Detail Siswa")
        # Di class ExtracurricularMonthlyReport
    week1_absence_id = fields.Many2one('extracurricular.absence', string='Absensi Minggu 1')
    week2_absence_id = fields.Many2one('extracurricular.absence', string='Absensi Minggu 2')
    week3_absence_id = fields.Many2one('extracurricular.absence', string='Absensi Minggu 3')
    week4_absence_id = fields.Many2one('extracurricular.absence', string='Absensi Minggu 4')
    week5_absence_id = fields.Many2one('extracurricular.absence', string='Absensi Minggu 5')

    @classmethod
    def generate_from_wizard(cls, wizard):
        absence_ids = [
            wizard.week1_absence_id,
            wizard.week2_absence_id,
            wizard.week3_absence_id,
            wizard.week4_absence_id,
            wizard.week5_absence_id,
        ]

        # Filter only valid absence records
        absence_ids = [a for a in absence_ids if a]

        # Ambil semua siswa dari ekskul terkait
        members = wizard.extracurricular_id.member_ids.filtered(lambda m: m.extracurricular_contact_type == 'student')

        report_lines = []
        for student in members:
            line_vals = {
                'partner_id': student.id,
                'week1_status': cls._get_status(student.id, wizard.week1_absence_id),
                'week2_status': cls._get_status(student.id, wizard.week2_absence_id),
                'week3_status': cls._get_status(student.id, wizard.week3_absence_id),
                'week4_status': cls._get_status(student.id, wizard.week4_absence_id),
                'week5_status': cls._get_status(student.id, wizard.week5_absence_id),
            }
            report_lines.append((0, 0, line_vals))

        report = cls.create({
            'name': f"Monthly Report {wizard.month}/{wizard.year} - {wizard.extracurricular_id.name}",
            'extracurricular_id': wizard.extracurricular_id.id,
            'month': wizard.month,
            'year': wizard.year,
            'report_line_ids': report_lines,
        })
        return report

    @staticmethod
    def _get_status(partner_id, absence):
        if not absence:
            return False
        line = absence.absence_line_ids.filtered(lambda l: l.partner_id.id == partner_id)
        return line.status if line else False
    
    def print_report(self):
        return self.env.ref('extracurricular_apps.action_report_monthly_extracurricular').report_action(self)



class ExtracurricularMonthlyReportLine(models.Model):
    _name = 'extracurricular.monthly.report.line'
    _description = 'Detail Laporan Bulanan Ekskul'

    report_id = fields.Many2one('extracurricular.monthly.report', string="Laporan", required=True, ondelete="cascade")
    partner_id = fields.Many2one('res.partner', string="Siswa", required=True)

    week1_status = fields.Selection([
        ('h', 'Hadir'),
        ('i', 'Izin'),
        ('s', 'Sakit'),
        ('a', 'Alpha')
    ], string='Minggu 1')

    week2_status = fields.Selection([
        ('h', 'Hadir'),
        ('i', 'Izin'),
        ('s', 'Sakit'),
        ('a', 'Alpha')
    ], string='Minggu 2')

    week3_status = fields.Selection([
        ('h', 'Hadir'),
        ('i', 'Izin'),
        ('s', 'Sakit'),
        ('a', 'Alpha')
    ], string='Minggu 3')

    week4_status = fields.Selection([
        ('h', 'Hadir'),
        ('i', 'Izin'),
        ('s', 'Sakit'),
        ('a', 'Alpha')
    ], string='Minggu 4')

    week5_status = fields.Selection([
        ('h', 'Hadir'),
        ('i', 'Izin'),
        ('s', 'Sakit'),
        ('a', 'Alpha')
    ], string='Minggu 5')
