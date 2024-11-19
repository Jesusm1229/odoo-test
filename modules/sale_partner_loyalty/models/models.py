# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order Points'

    # campo order_points calculado
    order_points = fields.Float(
        string='Loyalty Points Test',
        compute='_get_loyalty_points',
        store=True,  # para que se guarde en la base de datos
        help="Partner Loyalty Points Earned on this Order",
    )



    # metodo para calcular los puntos de lealtad
    # cada vez que se cambie el total de pedido se calcula
    @api.depends('amount_total', "coupon_point_ids")
    def _get_loyalty_points(self):
        for sale in self:
            print(f"sale {sale}")
            if sale.coupon_point_ids:
                # self.points is one to many relation
                points = sale.coupon_point_ids.mapped('points')
                sale.order_points = sum(points)
                print(f"order points {points}")
            else:
                sale.order_points = 0.0
