модули печатных форм адаптированы под версию 8.0, автор изменений @ivann, все вопросы к нему. Самостоятельно мы работоспособность не тестировали, поэтому модули предоставляются "как есть", без каких-либо гарантий работоспособности и вы можете использовать их на свой страх и риск

Замечание к установке. 
Поскольку я удалил из репозитория *.jasper файлы, то нужно предоставить openerp права на запись, чтобы эти файлы могли создаться в процессе работы

chown -R openerp:openerp modules/jasper_reports

**В целом состояние модулей для ветки 8.0 стоит оценивать как нестабильное. Некоторые модули могут не работать вообще, а некоторые не совсем как нужно. Будьте внимательны и учитывайте этот факт. Устанавливайте модули первоначально только на тестовую базу!**

для установки модуля sale с тестовыми данными пришлось сделать небольшой патч: account_invoice.py.diff