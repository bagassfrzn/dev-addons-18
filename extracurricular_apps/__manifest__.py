{
    'name': 'Extracurriculer Management Apps',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'ITClub SMKN 12 Jakarta',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'depends': [
        'base',
        'web'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/res_partner_views.xml',
        'views/res_extracurricular_views.xml',
        'views/menu_views.xml',
        'views/extracurricular_absence_views.xml',
        'views/monthly_report_wizard_views.xml',
        'views/monthly_report_views.xml',
        'views/report_monthly_report_templates.xml',
        'report/report.xml',
    ],
    'demo': [
        ''
    ],
    'auto_install': False,
    'application': True,
    'assets': {
        
    }
}