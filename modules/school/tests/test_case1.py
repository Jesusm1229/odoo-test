from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestSchool(TransactionCase):

    def setUp(self):
        super(TestSchool, self).setUp()
        self.School = self.env['school.student']
        self.SchoolClass = self.env['school.class']
        self.SchoolTeacher = self.env['school.teacher']

    def test_create_student(self):
        student = self.School.create({
            'name': 'Juan',
            'age': 20,
        })
        self.assertEqual(student.name, 'Juan')
        self.assertEqual(student.age, 20)

    def test_create_student_with_class(self):
        school_class = self.SchoolClass.create({
            'name': 'Math',
        })
        student = self.School.create({
            'name': 'Maria',
            'age': 22,
            'class_id': school_class.id,
        })
        self.assertEqual(student.name, 'Maria')
        self.assertEqual(student.age, 22)
        self.assertEqual(student.class_id.name, 'Math')

    def test_create_student_with_negative_age(self):
        with self.assertRaises(ValidationError):
            self.School.create({
                'name': 'Pedro',
                'age': -1,
            })

    def test_create_student_with_duplicate_name(self):
        self.School.create({
            'name': 'Carlos',
            'age': 25,
        })
        with self.assertRaises(ValidationError):
            self.School.create({
                'name': 'Carlos',
                'age': 30,
            })

    def test_create_class_with_teacher(self):
        teacher = self.SchoolTeacher.create({
            'name': 'Mr. Smith',
            'age': 40,
        })
        school_class = self.SchoolClass.create({
            'name': 'Science',
            'teacher_id': teacher.id,
        })
        self.assertEqual(school_class.name, 'Science')
        self.assertEqual(school_class.teacher_id.name, 'Mr. Smith')

    def test_create_teacher_with_negative_age(self):
        with self.assertRaises(ValidationError):
            self.SchoolTeacher.create({
                'name': 'Ms. Johnson',
                'age': -5,
            })