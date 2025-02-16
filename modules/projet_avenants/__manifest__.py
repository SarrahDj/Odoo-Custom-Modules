{
    'name': 'Avenants',
    'description': 'This module allows to add avenants to invoices',
    'depends': [ 'sale','base', 'sale_stock'],
    'data': [
      'views/avenant_view.xml',
        'views/sale_order_view.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',

    ],
    'installable': True,
    'application': False,

}
