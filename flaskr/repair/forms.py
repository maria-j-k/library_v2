from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, HiddenField, IntegerField, TextAreaField, SelectField, StringField, SubmitField
from wtforms.widgets import HiddenInput 
from wtforms.validators import DataRequired, AnyOf, Optional


class SearchForm(FlaskForm):
    name = StringField('Name')


class PublisherForm(FlaskForm):
    name = StringField('Name')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class SerieForm(FlaskForm):
    name = StringField('Name')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class CityForm(FlaskForm):
    name = StringField('Name')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class CollectionForm(FlaskForm):
    name = StringField('Name')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class LocationForm(FlaskForm):
    room = StringField('Name')
    shelf = StringField('Shelf')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class BookForm(FlaskForm):
    title = StringField('Title')
    isbn = StringField('ISBN')
    authors = StringField('Authors')
    publisher = StringField('Publisher')
    serie = StringField('Serie')
    city = StringField('Publication place')
    pub_year = StringField('Publication year')
    origin_language = StringField('Origin language')
    fiction = SelectField('Fiction', choices=[
                    ('', '---'),
                    (1, 'fiction'),
                    (0, 'non-fiction')
        ], 
        coerce=bool)
    literary_form = SelectField('Literary form', choices=[
                    ('', '---'),
                    ('PO', 'Poetry'),
                    ('PR', 'Prose'),
                    ('DR', 'Drama')
                ])
    genre = StringField('Genre')
    precision = TextAreaField('Precision')
    nukat = TextAreaField('NUKAT themes')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class PersonForm(FlaskForm):
    name = StringField('Name')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')
