# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_method = fields.Selection(
        string="Payment Method",
        selection=[
            ('cash', 'Cash'),
            ('credit_card', 'Credit Card'),
            ('check', 'Check')
        ],
        default='credit_card'
    )

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.payment_method == 'check':
                order.message_post(body="Please send the check to our address")
        return res


