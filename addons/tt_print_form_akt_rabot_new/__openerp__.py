{
    'name' : 'Akt vypolnennykh rabot QWeb',
    'version' : '0.1',
    'category' : 'Extra Reports',
    'author'  : 'Transparent Technologies Ltd.',
    'license' : 'AGPL-3',
    'depends' : ['base',
                 'l10n_ru',
                 'sale',
                 'tt_print_forms_common',
                 'tt_acc_invoice_line_subtotal_gross'],
    'installable': True,
    'auto_install': False,
    'description': '''
Модуль содержит QWeb шаблон для печати Акта выполненных работ. Печатать рекомендуется в firefox.
(в chromium проблемы с рендерингом, если размер таблицы работ превышает размер страницы )
============================================================
    ''',
    'data' : [
        'acc_inv_data.xml',
        'view/tt_print_form_akt_rabot.xml',
    ]

}
