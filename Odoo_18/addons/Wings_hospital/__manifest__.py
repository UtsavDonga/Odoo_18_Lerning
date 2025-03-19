{
    'name': 'Wings Hospital',
    'summary': 'Crud Prectise',
    'description': 'Hospital Management System',
    'author': 'The Hwak',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patients_views.xml',
        'views/appointments_views.xml',
        'views/patient_tag_views.xml',
        'views/doctors_views.xml',
        'views/menu.xml',
    ]
}