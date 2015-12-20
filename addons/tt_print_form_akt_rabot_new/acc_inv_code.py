# -*- coding: utf-8 -*-
import logging

from openerp.addons.tt_print_forms_common.pytils import numeral
from openerp.osv import osv, fields
from datetime import datetime
__logger = logging.getLogger(__name__)


class account_invoice(osv.Model):
    def _get_number_only(self, cr, uid, ids, field_name, arg, context):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            if not row.number:
                res[row.id] = '0'
                continue

            seq_id = self.pool.get('ir.sequence').search(cr, uid, [('code', '=', 'sale.order')])
            sequence = self.pool.get('ir.sequence').read(cr, uid, seq_id, ['padding', 'active'])[0]
            if sequence and sequence.get('active'):
                padding = sequence.get('padding')
                padding = 0 - int(padding)
                res[row.id] = row.number[padding:].lstrip('0')

        return res

    def _get_price_in_words(self, cr, uid, ids, field_name, arg, context):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            rubles = numeral.rubles(int(row.amount_total))
            copek_num = round(row.amount_total - int(row.amount_total))
            copek = numeral.choose_plural(int(copek_num), (u"копейка", u"копейки", u"копеек"))
            res[row.id] = ("%s %02d %s")%(rubles, copek_num, copek)

        return res

    def _get_invoices_count(self,cr,uid,ids,field,arg,context=None):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            res[row.id] = len(row.invoice_line)

        return res

    def _get_akt_date(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for row in self.browse(cr, uid, ids, context):
            date_object = datetime.strptime(row.date_invoice,'%Y-%m-%d')
            res[row.id] = date_object.strftime('%d.%m.%Y')
        return res

    def get_details(self, obj):
        str_res = u', '.join([obj.name_official_multi, obj.address_formatted])

        if hasattr(obj,'inn') and obj.inn:
           str_res = u', ИНН '.join([str_res, obj.inn])

        if hasattr(obj,'kpp') and obj.kpp:
           str_res = u', КПП '.join([str_res, obj.kpp])

        if hasattr(obj, 'bank_ids') and obj.bank_ids:
            if hasattr(obj.bank_ids,'acc_number') and obj.bank_ids.acc_number:
               str_res = u', р/сч '.join([str_res, obj.bank_ids.acc_number])

            if hasattr(obj.bank_ids,'bank_name]]') and obj.bank_ids.bank_name:
               str_res = u', банк '.join([str_res, obj.bank_ids.bank_name])

            if hasattr(obj.bank_ids,'bank_acc_corr]]') and obj.bank_ids.bank_acc_corr:
               str_res = u', корр. счет '.join([str_res, obj.bank_ids.bank_acc_corr])

            if hasattr(obj.bank_ids,'bank_bic]]')  and obj.bank_ids.bank_bic:
               str_res = u', БИК '.join([str_res, obj.bank_ids.bank_bic])
        return str_res



    _name = 'account.invoice'
    _inherit = 'account.invoice'
    _columns = {
        'number_only': fields.function(_get_number_only, type='char'),
        'price_in_words':fields.function(_get_price_in_words, type='char'),
        'invoices_count': fields.function(_get_invoices_count, type='integer'),
        'akt_date' :  fields.function(_get_akt_date, type='char'),
    }
account_invoice()