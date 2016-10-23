# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#    Copyright (C) 2012-2016 Noviat nv/sa (www.noviat.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_amount = fields.Float(
        digits=dp.get_precision('Account'),
        string='Total Discount Amount',
        readonly=True,
        store=True)
    discount_base_amount = fields.Float(
        digits=dp.get_precision('Account'),
        string='Base Amount before Discount',
        readonly=True,
        store=True)

    @api.multi
    def onchange_pricelist_id(self, pricelist_id, order_lines):
        res = super(SaleOrder, self).onchange_pricelist_id(
            pricelist_id, order_lines)
        sol_model = self.env['sale.order.line']
        for order_line in order_lines:
            if order_line[0] == 6:
                lines = sol_model.browse(order_line[2])
                for line in lines:
                    line._onchange_sale_discount()
        return res

    @api.multi
    def button_dummy(self):
        res = super(SaleOrder, self).button_dummy()
        self._compute_discount()
        return res

    def _compute_discount(self):

        if self.state != 'draft':
            return
        if self._context.get('discount_calc'):
            return

        grouped_discounts = {}
        line_discount_amounts = {}
        total_base_amount = 0.0
        line_updates = []

        for line in self.order_line:
            base_amount = line.price_unit * line.product_uom_qty
            total_base_amount += base_amount

            for discount in line.sale_discount_ids:
                if discount.discount_base == 'sale_order':
                    if discount.id not in grouped_discounts:
                        grouped_discounts[discount.id] = {
                            'sale_discount': discount,
                            'lines': [(line.id, base_amount)],
                            'disc_base_amt': base_amount}
                    else:
                        grouped_discounts[discount.id]['disc_base_amt'] \
                            += base_amount
                        grouped_discounts[
                            discount.id]['lines'].append(
                                (line.id, base_amount))
                else:
                    amt, pct = discount._calculate_discount(
                        line.price_unit, line.product_uom_qty)
                    line_discount_amounts[line.id] = amt
                    line_updates.append([1, line.id, {'discount': pct}])

        for entry in grouped_discounts.values():
            amt, pct = entry['sale_discount']._calculate_discount(
                entry['disc_base_amt'], 1.0)
            # redistribute the discount to the lines
            for line in entry['lines']:
                done = False
                pct_sum = pct
                for line_update in line_updates:
                    if line_update[1] == line[0]:
                        pct_sum = min(line_update[2]['discount'] + pct, 100.0)
                        line_update[2]['discount'] = pct_sum
                        done = True
                        break
                if not done:
                    line_updates.append(
                        (1, line[0], {'discount': pct_sum}))
                if line[0] not in line_discount_amounts:
                    line_discount_amounts[line[0]] = line[1] * pct / 100.0
                else:
                    line_discount_amounts[line[0]] = min(
                        line[1],
                        line_discount_amounts[line[0]]
                        + line[1] * pct / 100.0
                        )
        total_discount_amount = sum(line_discount_amounts.values())

        ctx = dict(self._context, discount_calc=True)
        self.with_context(ctx).write({
            'discount_amount': total_discount_amount,
            'discount_base_amount': total_base_amount,
            'order_line': line_updates,
            })

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for order in self:
            if not self._context.get('discount_calc'):
                order._compute_discount()
        return res
