# -*- coding: utf-8 -*-
{
    'name': "Oriflame",

    'summary': """
       Control Inventario Ariela Oriflame""",

    'description': """
        Que resulte hay yisus cristo amén    """,

    'author': "Ariela Oriflame",
    'website': "http://www.Orillama.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Insuranced',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
       # 'security/ir.model.access.csv',
        #'views/views.xml',
        'views/menu.xml',
        'views/proveedor.xml',
        'views/producto.xml',
        'views/tipo.xml',
        'views/pedido.xml',
        'views/detallepedido.xml',
        'reports/report_detallepedido.xml',
        #'views/cliente.xml',
       # 'views/factura.xml',
      #  'views/detalle_producto.xml',
	'security/ir.model.access.csv',	
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
