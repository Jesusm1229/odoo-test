# -*- coding: utf-8 -*-
# from odoo import http


# class Wizard(http.Controller):
#     @http.route('/wizard_test/wizard_test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wizard_test/wizard_test/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wizard_test.listing', {
#             'root': '/wizard_test/wizard_test',
#             'objects': http.request.env['wizard_test.wizard_test'].search([]),
#         })

#     @http.route('/wizard_test/wizard_test/objects/<model("wizard_test.wizard_test"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wizard_test.object', {
#             'object': obj
#         })

