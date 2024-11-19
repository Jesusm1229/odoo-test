# -*- coding: utf-8 -*-
# from odoo import http


# class SalePartnerLoyalty(http.Controller):
#     @http.route('/sale_partner_loyalty/sale_partner_loyalty', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_partner_loyalty/sale_partner_loyalty/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_partner_loyalty.listing', {
#             'root': '/sale_partner_loyalty/sale_partner_loyalty',
#             'objects': http.request.env['sale_partner_loyalty.sale_partner_loyalty'].search([]),
#         })

#     @http.route('/sale_partner_loyalty/sale_partner_loyalty/objects/<model("sale_partner_loyalty.sale_partner_loyalty"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_partner_loyalty.object', {
#             'object': obj
#         })

