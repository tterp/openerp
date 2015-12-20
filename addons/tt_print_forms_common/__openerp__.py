{
    'name' : 'TT-Print From\'s common files ',
    'version' : '0.1',
    'category' : 'Extra Reports',
    'author'  : 'Transparent Technologies Ltd.',
    'license' : 'AGPL-3',
    'depends' : ['base',
                 'l10n_ru'],
    'installable': True,
    'auto_install': False,
    'description': '''
This module adds Account Invoice Print Form.
============================================================
    ''',
    'data' : [
        'tt_print_forms_common_data.xml',
        'view/tt_print_forms_common_styles.xml',
    ]

}
