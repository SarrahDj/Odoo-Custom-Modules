{

'name': ' Gestion de Location bureau et de salles- Ajout des clients ',

'description': ' Gérer la location des clients ',

'author': 'BENHAMIDA Mustapha',

'depends': ['location_app'],
    'data': [

        'views/agence_clt.xml',
'views/locataire_menu.xml',
'views/locataire.xml',
        'security/ir.model.access.csv',
    ],

'application': False,

 }