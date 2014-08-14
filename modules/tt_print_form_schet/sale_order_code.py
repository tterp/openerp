# -*- coding: utf-8 -*-

import time
from openerp.report import report_sxw
from openerp.osv import osv, fields
from openerp.report.interface import report_int
from openerp.addons.jasper_reports import numeral


class sale_order_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_order_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update( {'time': time})

class account_invoice_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_invoice_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time})

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def _is_invoice(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context):
            res[row.id] = False
        return res

    # Parse order name. Strip order prefix and leading zeroes
    def _get_number_only(self, cr, uid, ids, field_name, arg, context):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            seq_id = self.pool.get('ir.sequence').search(cr, uid, [('code', '=', 'sale.order')])
            sequence = self.pool.get('ir.sequence').read(cr, uid, seq_id, ['padding', 'active'])[0]
            if sequence and sequence.get('active'):
                padding = sequence.get('padding')
                padding = 0 - int(padding)
                res[row.id] = row.name[padding:].lstrip('0')

        return res

    def _get_price_in_words(self, cr, uid, ids, field_name, arg, context):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            rubles = numeral.rubles(int(row.amount_total))
            copek_num = round((row.amount_total - int(row.amount_total))*100)
            copek = numeral.choose_plural(int(copek_num), (u"копейка", u"копейки", u"копеек"))
            res[row.id] = ("%s %02d %s")%(rubles, copek_num, copek)

        return res

    def _get_orders_count(self, cr, uid, ids, field, arg, context=None):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            res[row.id] = len(row.order_line)

        return res

    _columns = {
        'is_invoice': fields.function(_is_invoice, type='boolean'),
        'number_only': fields.function(_get_number_only, type='char'),
        'price_in_words':fields.function(_get_price_in_words, type='char'),
        'orders_count': fields.function(_get_orders_count, type='integer'),
    }
sale_order()


class account_invoice(osv.osv):
    def _get_number_only(self, cr, uid, ids, field_name, arg, context):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            if not row.number:
                raise osv.except_osv('Error!', 'You must confirm invoice!')

            seq_id = self.pool.get('ir.sequence').search(cr, uid, [('code', '=', 'sale.order')])
            sequence = self.pool.get('ir.sequence').read(cr, uid, seq_id, ['padding', 'active'])[0]
            if sequence and sequence.get('active'):
                padding = sequence.get('padding')
                padding = 0 - int(padding)
                res[row.id] = row.number[padding:].lstrip('0')

        return res

    def _is_invoice(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for row in self.browse(cr, uid, ids, context):
            res[row.id] = True
        return res

    def _get_price_in_words(self, cr, uid, ids, field_name, arg, context):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            rubles = numeral.rubles(int(row.amount_total))
            copek_num = round((row.amount_total - int(row.amount_total))*100)
            copek = numeral.choose_plural(int(copek_num), (u"копейка", u"копейки", u"копеек"))
            res[row.id] = ("%s %02d %s")%(rubles, copek_num, copek)

        return res

    def _get_invoices_count(self, cr, uid, ids, field, arg, context=None):
        res = {}

        for row in self.browse(cr, uid, ids, context):
            res[row.id] = len(row.invoice_line)

        return res
    def invoice_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.invoice.schet',
            'datas': datas,
            'nodestroy' : True
        }

    _name = 'account.invoice'
    _inherit = 'account.invoice'
    _columns = {
        'is_invoice': fields.function(_is_invoice, type='boolean'),
        'number_only': fields.function(_get_number_only, type='char'),
        'price_in_words':fields.function(_get_price_in_words, type='char'),
        'invoices_count': fields.function(_get_invoices_count, type='integer'),
    }
account_invoice()
