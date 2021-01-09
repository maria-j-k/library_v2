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
