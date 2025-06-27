from odoo import models, fields, api
from datetime import date
import calendar


class ExtracurricularMonthlyReportWizard(models.TransientModel):
    _name = 'extracurricular.monthly.report.wizard'
    _description = 'Wizard Generate Laporan Bulanan Ekskul'

    extracurricular_id = fields.Many2one(
        'res.extracurricular',
        string='Ekskul',
        required=True
    )

    month = fields.Selection(
        selection=[(str(i), f'{i:02}') for i in range(1, 13)],
        string='Bulan',
        required=True
    )

    year = fields.Integer(
        string='Tahun',
        required=True,
        default=lambda self: fields.Date.today().year
    )

    # Helper untuk domain
    start_date = fields.Date(string='Tanggal Awal', compute='_compute_date_range', store=True)
    end_date = fields.Date(string='Tanggal Akhir', compute='_compute_date_range', store=True)

    # Mingguan
    week1_absence_id = fields.Many2one('extracurricular.absence', string='Minggu 1')
    week2_absence_id = fields.Many2one('extracurricular.absence', string='Minggu 2')
    week3_absence_id = fields.Many2one('extracurricular.absence', string='Minggu 3')
    week4_absence_id = fields.Many2one('extracurricular.absence', string='Minggu 4')
    week5_absence_id = fields.Many2one('extracurricular.absence', string='Minggu 5')

    @api.depends('month', 'year')
    def _compute_date_range(self):
        for rec in self:
            if rec.month and rec.year:
                month = int(rec.month)
                rec.start_date = date(rec.year, month, 1)
                last_day = calendar.monthrange(rec.year, month)[1]
                rec.end_date = date(rec.year, month, last_day)
            else:
                rec.start_date = False
                rec.end_date = False

    def action_generate_report(self):
        self.ensure_one()

        # Ambil semua absence_id valid
        absences = [
            self.week1_absence_id,
            self.week2_absence_id,
            self.week3_absence_id,
            self.week4_absence_id,
            self.week5_absence_id
        ]

        # Gabungkan partner yang ikut di salah satu absensi
        student_ids = set()
        absence_dict = {}  # mapping: week -> {partner_id: status}

        for week_index, absence in enumerate(absences, start=1):
            if not absence:
                continue
            lines = absence.absence_line_ids.filtered(lambda l: l.partner_id.extracurricular_contact_type == 'student')
            absence_dict[week_index] = {line.partner_id.id: line.status for line in lines}
            student_ids.update(absence_dict[week_index].keys())

        # Buat report bulanan utama
        report = self.env['extracurricular.monthly.report'].create({
            'name': f'Report {self.extracurricular_id.name} - {self.month}/{self.year}',
            'extracurricular_id': self.extracurricular_id.id,
            'month': self.month,
            'year': self.year,
            'week1_absence_id': self.week1_absence_id.id,
            'week2_absence_id': self.week2_absence_id.id,
            'week3_absence_id': self.week3_absence_id.id,
            'week4_absence_id': self.week4_absence_id.id,
            'week5_absence_id': self.week5_absence_id.id,
        })

        # Buat line per siswa
        lines_to_create = []
        for student_id in student_ids:
            vals = {
                'report_id': report.id,
                'partner_id': student_id,
                'week1_status': absence_dict.get(1, {}).get(student_id),
                'week2_status': absence_dict.get(2, {}).get(student_id),
                'week3_status': absence_dict.get(3, {}).get(student_id),
                'week4_status': absence_dict.get(4, {}).get(student_id),
                'week5_status': absence_dict.get(5, {}).get(student_id),
            }
            lines_to_create.append(vals)

        self.env['extracurricular.monthly.report.line'].create(lines_to_create)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Monthly Report',
            'res_model': 'extracurricular.monthly.report',
            'res_id': report.id,
            'view_mode': 'form',
            'target': 'current',
        }

