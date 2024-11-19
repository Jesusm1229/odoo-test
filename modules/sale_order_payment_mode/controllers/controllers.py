# -*- coding: utf-8 -*-
# from odoo import http


# class Modulo1(http.Controller):
#     @http.route('/sale_order_payment_mode/sale_order_payment_mode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_payment_mode/sale_order_payment_mode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_payment_mode.listing', {
#             'root': '/sale_order_payment_mode/sale_order_payment_mode',
#             'objects': http.request.env['sale_order_payment_mode.sale_order_payment_mode'].search([]),
#         })

#     @http.route('/sale_order_payment_mode/sale_order_payment_mode/objects/<model("sale_order_payment_mode.sale_order_payment_mode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_payment_mode.object', {
#             'object': obj
#         })

