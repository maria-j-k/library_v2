from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, HiddenField, IntegerField, TextAreaField, SelectField, StringField, SubmitField
from wtforms.widgets import HiddenInput 
from wtforms.validators import DataRequired, AnyOf, Optional

class TitleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Next')


class PersonForm(FlaskForm):
    name = StringField('Name')
    role = HiddenField(validators=[AnyOf(values=['A', 'T', 'R', 'I'])])
    id_ = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])

    def __init__(self, *args, **kwargs):
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(PersonForm, self).__init__(*args, **kwargs)


class CreatorsForm(FlaskForm):
#    title = StringField('Title', render_kw={'readonly': True})
    title = StringField('Title')
    authors = FieldList(FormField(PersonForm, default={'role': 'A'}), min_entries=3)
    translators = FieldList(FormField(PersonForm, default={'role': 'T'}), min_entries=3 )
    redactors = FieldList(FormField(PersonForm, default={'role': 'R'}), min_entries=3)
    intro = FieldList(FormField(PersonForm, default={'role': 'I'}), min_entries=3)
    submit = SubmitField('Submit')

class PublisherForm(FlaskForm):
    name = StringField('Name') # autocomplete z możliwością wpisania    
    serie = StringField('Serie') # autocomplete z możliwością wpisania
    pub_year = StringField('Publication date') # regex validator


class BookForm(FlaskForm):
    pass


class CopyForm(FlaskForm):
    pass
