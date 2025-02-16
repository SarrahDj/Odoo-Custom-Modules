{
'name': ' Gestion de Location bureau et de salles ',
'description': ' Gérer une agence de location de Bureaux et de salles ',
'author': 'BENHAMIDA Mustapha',
'depends': ['base'],
'data': [
   'security/agence_security.xml',
   'security/ir.model.access.csv',
   'views/agence_menu.xml',
   'views/agence_view.xml',
       ],
'installable': True,
'application': True,
'description_image': '/location_app/static/description/client_company.png',
}
