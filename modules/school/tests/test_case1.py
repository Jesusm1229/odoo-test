from odoo.tests.common import TransactionCase

class test_school(TransactionCase):

    def setUp(self):
        super(test_school, self).setUp()

    def test_create_student(self):
        student = self.env['school.student'].create({
            'name': 'Juan',
            'age': 20,
        })
        self.assertEqual(student.name, 'Juan')
        self.assertEqual(student.age, 20)