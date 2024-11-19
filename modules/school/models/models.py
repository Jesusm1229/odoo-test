# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError

from odoo import models, fields, api


class School(models.Model):
    _name = 'school.student'
    _description = 'tabla de estudiantes'

    name = fields.Char(string="Nombre", required=True)
    age = fields.Integer(string='Edad')
    class_id = fields.Many2one('school.class', string='Class')

    # _sql_constraints = [
    #     ('name_uniq', 'unique(name)', "El nombre del estudiante ya existe !"),
    #     ('no_age_negative', 'CHECK(age >= 0)', "La edad del estudiante no puede ser negativa !"),
    # ]

    # API constraint with the sql constraint
    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            if self.search_count([('name', '=', record.name.lower()), ('id', '!=', record.id)]) > 0:
                raise ValidationError("El nombre del estudiante ya existe !")

    @api.constrains('age')
    def _check_age_non_negative(self):
        for record in self:
            if record.age < 0:
                raise ValidationError("La edad del estudiante no puede ser negativa !")


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'tabla de clases'

    name = fields.Char(string="Nombre", required=True)
    teacher_id = fields.Many2one('school.teacher', string='Profesor')
   # student_ids = fields.One2many('school.student', 'class_id', string='Estudiantes')


class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'tabla de profesores'

    name = fields.Char(string="Nombre", required=True)
    age = fields.Integer(string='Edad')
    class_ids = fields.Many2many('school.class',  string='Clases')

    @api.constrains('age')
    def _check_age_non_negative(self):
        for record in self:
            if record.age < 0:
                raise ValidationError("La edad del profesor no puede ser negativa !")