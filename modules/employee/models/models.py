# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Employee(models.Model):
    _name = "company.employee"
    _rec_name = "name"

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    phone = fields.Char(string="Phone")

    verified = fields.Boolean(string="Verified", default=False)

    def act_confirm(self):
        self.write({'verified': True})
        return True


class Partner(models.Model):
    _inherit = 'res.partner'

    company_management_id = fields.One2many('company.employee', 'partner_id', string="Employee")


