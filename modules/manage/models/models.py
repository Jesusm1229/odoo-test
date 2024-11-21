# -*- coding: utf-8 -*-
import logging
from datetime import timedelta

from unicodedata import category

from odoo import models, fields, api
from odoo.api import readonly
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import datetime

_logger = logging.getLogger(__name__)


class Developer(models.Model):
    # herencia de clase. Cuando se usa el _inherit junto con el mismo _name del objeto se crea una extensión. Si el name cambia  se crea un objeto nuevo con su propia database y es ignorada por vistas existentes
    # _name = 'res.partner'
    _inherit = 'res.partner'

    # crearemos si el usuario que se crea es developer o no
    is_dev = fields.Boolean()

    technology_ids = fields.Many2many('manage.technology',
                                      relation='developer_tecnhologies',
                                      column1='developer_id',
                                      column2='technology_id',
                                      string="Technologies"
                                      )

    task_ids = fields.One2many('manage.task', 'developer', string="Tasks")

    # Cuando cambie el is_dev. Para buscar el category name vas a tech. Modelo res.partner y ves el campo name
    @api.onchange('is_dev')
    def _onchange_is_dev(self):
        categories = self.env['res.partner.category'].search([('name', '=', 'Developer')])
        if len(categories) > 0:
            category = categories[0]
        else:
            category = self.env['res.partner.category'].create({'name': 'Developer'})
        # si es developer se añade la categoría. Category es un campo many2many. El 4 es añadir y el 3 es quitar
        self.category_id = [(4, category.id)]  # if self.is_dev else [(3, category.id)]


class Project(models.Model):
    _name = 'manage.project'
    _description = 'Manage Project'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    history_ids = fields.One2many('manage.history', 'project_id', string="Histories")


class History(models.Model):
    _name = 'manage.history'
    _description = 'Manage History'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    project_id = fields.Many2one('manage.project', ondelete='set null', string="Project")

    task_ids = fields.One2many('manage.task', 'history_id', string="Tasks")

    # used technologies
    technology_ids = fields.Many2many('manage.technology', compute='_get_technologies', store=True,
                                      string="Technologies")

    # se recorren todas las tareas y se obtienen las tecnologias asociadas
    @api.depends('task_ids')
    def _get_technologies(self):
        # Iterate over each history record
        for history in self:
            technologies = []
            # Iterate over each task in the history
            for task in history.task_ids:
                # If technologies list is empty, assign task.technology_ids to it
                if not technologies:
                    technologies = task.technology_ids
                else:
                    # Otherwise, append task.technology_ids to technologies
                    technologies = technologies + task.technology_ids
            # Assign the accumulated technologies to history.technology_ids
            history.technology_ids = technologies


class Task(models.Model):
    # modulo mange.task
    _name = 'manage.task'
    _description = 'Manage Task'

    code = fields.Char(compute='_get_code', store=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    # creation_date = fields.Date(string="Creation Date", default=fields.Date.today)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    is_paused = fields.Boolean(string="Is Paused", default=False)

    history_id = fields.Many2one('manage.history', ondelete='set null', string="History")

    # calculate the sprint opened for the task. The user wont select the sprint, it will be calculated
    # sprint_id = fields.Many2one('manage.sprint', ondelete='set null',  string="Sprint")

    # adding store true to make it store on DB just one. Cuando que se crea el sprint cuando se genere el código
    sprint_id = fields.Many2one('manage.sprint', ondelete='set null', compute='_get_sprint', store=True,
                                string="Sprint")

    # many tasks can use many technologies
    technology_ids = fields.Many2many('manage.technology',
                                      # adding relation table for a more optimized query
                                      relation='task_technology_rel',
                                      column1='task_id',
                                      column2='technology_id',
                                      string="Technologies")

    # campo relacional no almacenado en DB
    project_id = fields.Many2one('manage.project', related='history_id.project_id', readonly=True, string="Project")

    # añadiendo un campo many2one para el desarrollador. Muchas tareas pueden ser asignadas a un desarrollador
    # developer_id = fields.Many2one('res.partner', string="Developer")

    # cambiaremos el developer_id para permitir muchos developers
    developer_ids = fields.Many2many('res.partner', string="Developers")

    # get code of the task
    # @api.one
    def _get_code(self):
        for task in self:
            try:
                # el codigo de cada tarea se genera independiente del sprint
                # if len(task.sprint_id) == 0:
                task.code = 'Tsk_' + str(task.id)
                # else:
                #     task.code = str(task.sprint_id.name).upper() + '_' + str(task.id)
                _logger.debug("Code generated successfully" + task.code)
            except:
                raise ValidationError("Error in code generation")

    @api.depends('code')
    def _get_sprint(self):  # a task collection
        for task in self:
            # searh sprints associated to the project.
            sprints = self.env['manage.sprint'].search([('project_id', '=', task.history_id.project_id.id)])
            # we need to check which sprint is opeened
            found = False
            for sprint in sprints:
                # checking if sprint is opened
                if isinstance(sprint.end_date, datetime.datetime) and sprint.end_date > datetime.datetime.now():
                    task.sprint_id = sprint.id
                    found = True
            if not found:
                task.sprint_id = False
                raise ValidationError("No opened sprint found for the task")

    def _get_definition_date(self):
        return datetime.Datetime.now()

    # campo fecha de definicion. A diferencia de los campos computados, los default toman el valor una vez
    # definition_date = fields.Datetime(default=_get_definition_date(), string="Definition Date")
    definition_date = fields.Datetime(default=lambda self: fields.Datetime.now(), string="Definition Date")


# Modelo con herencia prototípica. Se crea una tabla que con los mismos atributos más los nuevos.
class Bug(models.Model):
    _name = 'manage.bug'
    _description = 'Manage Bug'
    _inherit = 'manage.task'  # se copian todos los atributos a esta nueva tabla

    # se copia de task. Odoo
    technology_ids = fields.Many2many('manage.technology',
                                      # adding relation table for a more optimized query
                                      relation='task_technology_rel_bugs',
                                      column1='bug_id',
                                      column2='technology_id',
                                      string="Technologies")

    task_linked = fields.Many2many('manage.task',
                                   # adding relation table for a more optimized query
                                   relation='task_bugs',
                                   column1='bug_id',
                                   column2='task_id',
                                   string="Tasks")

    # relacion con bugs
    bug_linked = fields.Many2many('manage.bug',
                                  # adding relation table for a more optimized query
                                  relation='bugs_bugs',
                                  column1='bug1_id',
                                  column2='bug2_id',
                                  string="Bugs")

    improvement_linked = fields.Many2many('manage.improvement',
                                          # adding relation table for a more optimized query
                                          relation='bugs_improvements',
                                          column1='bug_id',
                                          column2='improvement_id',
                                          string="Improvements")

    developer_ids = fields.Many2many('res.partner',
                                     # adding relation table for a more optimized query
                                     relation='developers_bugs',
                                     column1='bug_id',
                                     column2='developer_id',
                                     string="Developers")


# Modelo con herencia prototípica. Se crea una tabla que con los mismos atributos más los nuevos.
class Improvement(models.Model):
    _name = 'manage.improvement'
    _description = 'Manage Improvement'
    _inherit = 'manage.task'  # se copian todos los atributos a esta nueva tabla

    # se copia de task. Odoo
    technology_ids = fields.Many2many('manage.technology',
                                      # adding relation table for a more optimized query
                                      relation='task_technology_rel_improvements',
                                      column1='improvement_id',
                                      column2='technology_id',
                                      string="Technologies")

    # relacion con bugs
    history_linked = fields.Many2many('manage.history')

    developer_ids = fields.Many2many('res.partner',
                                     # adding relation table for a more optimized query
                                     relation='developers_improvements',
                                     column1='improvement_id',
                                     column2='developer_id',
                                     string="Developers")


class Sprint(models.Model):
    _name = 'manage.sprint'
    _description = 'Manage Sprint'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    duration = fields.Integer(string="Duration", default=15)

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(compute='_get_end_date', store={True}, string="End Date")

    task_ids = fields.One2many('manage.task', 'sprint_id', string="Tasks")

    project_id = fields.Many2one('manage.project', ondelete='set null', string="Project")

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for sprint in self:
            try:
                if isinstance(sprint.start_date, datetime.datetime) and sprint.duration > 0:
                    sprint.end_date = sprint.start_date + datetime.timedelta(days=sprint.duration)
                else:
                    sprint.end_date = sprint.start_date
                _logger.debug("End date calculated successfully")
            except:
                raise ValidationError("Error in end date calculation")


class Technology(models.Model):
    _name = 'manage.technology'
    _description = 'Manage Technology'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    photo = fields.Image(max_width=200, max_height=200, string="Photo")

    task_ids = fields.Many2many('manage.task',
                                relation='task_technology_rel',
                                column1='technology_id',
                                column2='task_id',
                                string="Tasks")
