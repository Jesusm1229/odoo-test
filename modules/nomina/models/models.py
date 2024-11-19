# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Nomina(models.Model):
    _name = 'nomina.nomina'
    _description = 'nomina de empleados'

    name = fields.Char()
    value = fields.Integer()

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "El nombre de la nomina ya existe !"),
        ('no_value_negative', 'CHECK(value >= 0)', "El valor de la nomina no puede ser negativo !"),
    ]

    # @api.model
    # def create(self, vals):
    #     if vals.get('value') < 0:
    #         raise ValueError('El valor de la nomina no puede ser negativo !')
    #     return super(Nomina, self).create(vals)


