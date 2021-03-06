from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import BooleanField, FieldList, FormField, HiddenField, IntegerField, TextAreaField, SelectField, StringField, SubmitField
from wtforms.widgets import HiddenInput 
from wtforms.validators import DataRequired, AnyOf, Optional

from flaskr.models import Publisher, Room

class SearchForm(FlaskForm):
    name = StringField('Name')


class PublisherForm(FlaskForm):
    name = StringField('Name')
    name_id = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


def all_publishers():
    return Publisher.query.all()


class SerieForm(FlaskForm):
    name = StringField('Name')
    name_id = HiddenField(validators=[Optional(strip_whitespace=True)])
    publisher = QuerySelectField(query_factory=all_publishers, allow_blank=False)
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class CityForm(FlaskForm):
    name = StringField('Name')
    name_id = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class CollectionForm(FlaskForm):
    name = StringField('Name')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class RoomForm(FlaskForm):
    name = StringField('Name')
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


def all_rooms():
    return Room.query.all()


class ShelfForm(FlaskForm):
    name = StringField('Name')
    room = QuerySelectField(query_factory=all_rooms, allow_blank=False)
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Sumbit')


class BookForm(FlaskForm):
    title = StringField('Title')
    isbn = StringField('ISBN')
#    authors = StringField('Authors')
#    translation = StringField('Translation')
#    redaction = StringField('Redaction')
#    introduction = StringField('Introduction')
    publisher = StringField('Publisher')
    publisher_id = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    serie = StringField('Serie')
    serie_id = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    city = StringField('Publication place')
    city_id = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
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
    name_id = HiddenField(validators=[Optional(strip_whitespace=True)])
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')
    submit = SubmitField('Submit')


class Person2Form(FlaskForm):
    name = StringField('Name')
#    person_id = IntegerField(widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    name_id = HiddenField(validators=[Optional(strip_whitespace=True)])
    role = HiddenField(validators=[AnyOf(values=['A', 'T', 'R', 'I'])])
    incorrect = BooleanField('Incorrect')
    approuved = BooleanField('Approuved')

    class Meta:
        csrf = False


class CreatorForm(FlaskForm):
    creators = FieldList(FormField(Person2Form, default={'role': 'A'}), max_entries=3)
    submit = SubmitField('Sumbit')
    
