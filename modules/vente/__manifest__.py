{

'name': ' Ventes patch  ',

'description': '  ',

'author': 'SARAH',

'depends': ['sale', 'stock'],
    'data': [
        'views/vente_view.xml',
        'wizard/sale_analysis_wizard_view.xml',
        'views/sale_analysis_wizard_menu.xml',
        'security/ir.model.access.csv',
        'data/sale_order_report_data.xml',
        'report/sale_order_report_template.xml',
        'views/stock_picking_menu.xml',
        'views/stock_analysis_view.xml',
        'report/surface_analysis_report_template.xml',
    ],
'installable': True,
'application': False,

 }