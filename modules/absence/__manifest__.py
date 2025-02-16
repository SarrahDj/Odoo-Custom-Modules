{
    'name': 'Autorisation d\'absences',
    'version': '13.0.1.0.0',
    'summary': 'Module for managing absence authorizations',
    'description': 'This module allows for the management of absence authorizations for employees.',
    'category': 'Human Resources',
    'depends': ['hr'],
    'data': [
        'views/absence_view.xml',
        'views/report_template.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
