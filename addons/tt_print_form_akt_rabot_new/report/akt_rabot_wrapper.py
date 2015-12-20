# -*- coding: utf-8 -*-

from openerp import api, models
#
# Причины замены стандартного translate_doc
# 1. При вызове стандартного translate_doc возникают проблемы с подгрузкой css при печати pdf.
#    !!!! НО wrapper проблему не решил
#    ( https://github.com/odoo/odoo/issues/2934
#      https://github.com/odoo/odoo/pull/3260)
# 2. Не удается отключить стандартные заголовоки из report/view/layouts.xml
# (наследование от external_layout_header и external_layout_footer приводит к изменению ВСЕХ отчетов)
# Так что заменяем вызов translate_doc и устанавливаем нужный контекст, в котором будет выполняться отчет
#

class akt_rabot_report(models.AbstractModel):
    _name = 'report.tt_print_form_akt_rabot_new.tt_print_form_akt_rabot_wrapper'

    # HINT интересно попробовать с @api.multi
    # Устанавливаем в контекст объект, с которым будем работать !!
    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        acc_invoice_obj = self.pool['account.invoice']
        selected_obj = acc_invoice_obj.browse(cr, uid, ids, context=context)
        for obj in selected_obj:
            o = obj
        docargs = {
            'o' : o
        }
        return report_obj.render(cr, uid, ids, 'tt_print_form_akt_rabot_new.tt_print_form_akt_rabot_document', docargs, context=context)

