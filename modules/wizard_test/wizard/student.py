from odoo import models, fields, api


class StudentWizardTest(models.TransientModel):
    _name = 'wizard_test.test'
    _description = 'Student Wizard Test'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)

    def print_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref('wizard_test.action_report_student').report_action(self, data=data)

