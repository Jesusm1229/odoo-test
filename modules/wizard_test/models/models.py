# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class wizard_test(models.Model):
#     _name = 'wizard_test.wizard_test'
#     _description = 'wizard_test.wizard_test'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

