# -*- coding: utf-8 -*-
{
    'name' : 'Pedidos tipo muestra',
    'version' : '1',
    'description': """
        Permite la creacion de pedidos de venta tipo muestra
    """,
    'category' : 'Sale',
    'depends' : ['sale_stock'],
    'data': [
        'sale_view.xml',
        #'security/groups.xml',
        #'security/ir.model.access.csv',
        
    ],
    'demo': [

    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
