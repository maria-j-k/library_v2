from flask_security import RegisterForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


#class ReaderRegisterForm(RegisterForm):
#    first_name = StringField('First Name', [DataRequired()])
#    last_name = StringField('Last Name', [DataRequired()])
##    school = nazwa szkoły - wybierana z listy
##    division = nazwa klasy
##    start_year
#    role = SelectField('Role', choices=[
#            ('visitor', 'Visitor'),
#            ('student', 'Student'),
#            ('teacher', 'Teacher'),
#            ('librarian', 'Librarian'),
#        ])
#


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
#    school = nazwa szkoły - wybierana z listy
#    division = nazwa klasy
#    start_year
    role = SelectField('Role', choices=[
            ('visitor', 'Visitor'),
            ('student', 'Student'),
            ('teacher', 'Teacher'),
            ('librarian', 'Librarian'),
        ])


    @security.register_context_processor
    def security_register_processor():
        return dict(register_form=ExtendedRegisterForm, msg='Działa')    





