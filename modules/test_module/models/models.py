# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WorkActivity(models.Model):
    _name = "work.activity"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    work_activity_line_ids = fields.One2many('work.activity.line', 'work_activity_id', string="Work Activity Line")

    active = fields.Boolean(string="Active", default=False)



class WorkActivityLine(models.Model):
    _name = 'work.activity.line'

    sub_activity = fields.Char(string="Name", required=True)
    deadline = fields.Date(string="Deadline", required=True)
    work_activity_id = fields.Many2one('work.activity', string="Work Activity")




