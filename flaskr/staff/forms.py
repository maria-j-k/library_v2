from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, TextAreaField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class TitleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Next')

class PersonForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Submit')

class CreatorsForm(FlaskForm):
    person = FieldList(StringField('Name', validators=[DataRequired()]), min_entries=3, max_entries=12)
    submit = SubmitField('Submit')
