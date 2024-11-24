# -*- coding: utf-8 -*-
import logging
import re
from datetime import timedelta

from unicodedata import category

from odoo import models, fields, api
from odoo.api import readonly
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import datetime


_logger = logging.getLogger(__name__)

#Herencia clásica: Se extiende la misma tabla con los mismos atributos más los nuevos. SÓLO SE USA INHERIT
#Herencia prototípica: Se crea una tabla nueva con los mismos atributos más los nuevos. SE USA INHERIT Y NAME
#Herencia por delegación: Se crea una tabla nueva con los mismos atributos más los nuevos. SE USA INHERIts


class Developer(models.Model):
    # herencia de clase. Cuando se usa el _inherit junto con el mismo _name del objeto se crea una extensión.
    # Si el name cambia  se crea un objeto nuevo con su propia database y es ignorada por vistas existentes
    # NOTA: si usas el mismo nombre y la inherit, entonces la herencia será clásica
    _name = 'res.partner'
    _inherit = 'res.partner'

    # crearemos si el usuario que se crea es developer o no
    is_dev = fields.Boolean()

    access_code = fields.Char(string="Access Code")

    technology_ids = fields.Many2many('manage.technology',
                                      relation='developer_technologies',
                                      column1='developer_id',
                                      column2='technology_id',
                                      string="Technologies"
                                      )
    task_ids = fields.Many2many('manage.task',
                                'developer_tasks_rel',
                                'developer_id',
                                'task_id',
                                string="Tasks")

    bug_ids = fields.Many2many('manage.bug',
                               'developer_bugs_rel',
                               'developer_id',
                               'bug_id',
                               string="Bugs")

    improvement_ids = fields.Many2many('manage.improvement',
                                        'developer_improvements_rel',
                                        'developer_id',
                                        'improvement_id',
                                        string="Improvements")


    #task_ids = fields.One2many('manage.task', 'developer_id', string="Tasks")

    @api.constrains
    def _check_code(self):
        regex = re.compile('^[0-9]{8}[a-z]', re.I)
        for dev in self:
            if regex.match(dev.access_code):
                _logger.info('Código de acceso generado correctamente')
            else:
                raise ValidationError('Formato de código de acceso incorrecto')


    #diferncia entre una vista y una tupla. La vista se puede modificar los elementos de la vista. La tupla no
    #Se pueden concatenar restricciones [(), ()] para que se cumplan todas las tuplas.
    _sql_constraints = [(
       'access_code_unique',
        'UNIQUE(access_code)',
        'El código de acceso debe ser único'
    )]



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

from odoo import models, fields, api

#testing model view of sql
class DeveloperReport(models.Model):
    _name = 'developer.report'
    _auto = False  # This indicates that the model is not associated with a database table

    name = fields.Char(string="Developer Name")
    task_count = fields.Integer(string="Task Count")

    #La vista no sirve porque no existen las tablas.
    #Este es sólo un ejemplo para mostrar cómo se puede hacer una vista en Odoo
    # def init(self):
    #     self.env.cr.execute("""
    #         CREATE OR REPLACE VIEW developer_report AS (
    #             SELECT
    #                 row_number() OVER () AS id,
    #                 rp.name AS name,
    #                 COUNT(mt.id) AS task_count
    #             FROM
    #                 res_partner rp
    #             LEFT JOIN
    #                 developers_tasks_rel dtr ON rp.id = dtr.developer_id
    #             LEFT JOIN
    #                 manage_task mt ON dtr.task_id = mt.id
    #             WHERE
    #                 rp.is_dev = True
    #             GROUP BY
    #                 rp.name
    #         )
    #     """)


class Project(models.Model):
    _name = 'manage.project'
    _description = 'Manage Project'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    history_ids = fields.One2many('manage.history', 'project_id', string="Histories")


#Fallo en el modelo historia desde la vista de PRODUCTOS. Si desde acá deseas agregar una tarea, no se puede. Acá entra NewId

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

    project_id = fields.Many2one('manage.project', related='history_id.project_id', readonly=True, string="Project")
    code = fields.Char(compute='_get_code', store=True)
    name = fields.Char(string="Name", required=True, help="Introduce the name of the task")
    description = fields.Text(string="Description")
    # creation_date = fields.Date(string="Creation Date", default=fields.Date.today)
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
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
    #project_id = fields.Many2one('manage.project', related='history_id.project_id', readonly=True, string="Project")

    # añadiendo un campo many2one para el desarrollador. Muchas tareas pueden ser asignadas a un desarrollador
    #developer_id = fields.Many2one('res.partner', string="Developer")

    # cambiaremos el developer_id para permitir muchos developers
    #developer_ids = fields.Many2many('res.partner', string="Developers")

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
            #esto genera un error en la vista de PRODUCTOS porque el id no está gnerado todavía.
            #Cuando no se ha generado Odoo devuelve un NewId
            #sprints = self.env['manage.sprint'].search([('project_id', '=', task.history_id.project_id.id)])
            #se revisa si la historia tiene un id generado, de lo contrario se usa el origin
            if isinstance(task.history_id.project_id, models.NewId):
                id_project = int(task.history_id.project_id.origin)
            else:
                id_project = task.history_id.project_id.id
            sprints = self.env['manage.sprint'].search([('project_id', '=', id_project)])
            # we need to check which sprint is opened
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

    # Función usada para traer el developer del contexto actual
    def _get_default_dev(self):
        dev = self.browse(self.env.context.get('current_developer'))
        if dev:
            return [dev.id]
        else:
            return []


    developer_ids = fields.Many2many('res.partner',
                                    relation='developers_tasks_rel',
                                    column1='task_id',
                                    column2='developer_id',
                                    string="Developer",
                                    default=_get_default_dev #es default porque se ejecuta una vez. El computado se ejecuta siempre
                                    )





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

    # Define the compute method
    #en odoo un campo sin valor es booleano.
    @api.depends('start_date', 'duration')
    def _compute_active(self):
        for sprint in self:
            sprint.active = sprint.start_date <= fields.Datetime.now() <= sprint.end_date

    active = fields.Boolean(string="Active", compute='_compute_active', store=True)

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
