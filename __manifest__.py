# -*- coding: utf-8 -*-
{
    'name': "Enzapps Petroleum Updation",
    'author':
        'Enzapps Private Limited',
    'summary': """
This module is for adding some missing functionality to 'EnzPetroleum' Module 
""",

    'description': """
This module is for adding some missing functionality to 'EnzPetroleum' Module 
    """,
    "live_test_url": '',
    "website": "https://www.enzapps.com",
    'category': 'base',
    'version': '14.0',
    'depends':['base', 'account', 'stock','stock_account', 'product','sale', 'sale_management', 'purchase','contacts','hr','enz_petroleum'],
    "images": ['static/description/icon.png'],
    'data': [
        "views/updation.xml",
        "views/expense.xml",
    ],
    'demo': [],
    'installable': True,
    'application': True,
    "price": '100',
    "currency": 'USD',
}
