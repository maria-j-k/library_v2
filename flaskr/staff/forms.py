from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import BooleanField, FieldList, FormField, HiddenField, IntegerField, TextAreaField, SelectField, StringField, SubmitField
from wtforms.widgets import HiddenInput 
from wtforms.validators import DataRequired, AnyOf, Optional

from flaskr.models import Collection, Location



class TitleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Next')


class PersonForm(FlaskForm):
    name = StringField('Name')
    role = HiddenField(validators=[AnyOf(values=['A', 'T', 'R', 'I'])])
    id_ = HiddenField()
#    id_ = IntegerField(widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])

    class Meta:
        csrf = False


class PublisherForm(FlaskForm):
    publisher_name = StringField('Publisher') # autocomplete z możliwością wpisania    
    id_ = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    city = StringField('Publication place') # autocomplete z możliwością wpisania 
    c_id_ = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    serie = StringField('Serie') # autocomplete z możliwością wpisania
    s_id_ = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])

    class Meta:
        csrf = False


class BookForm(FlaskForm):
    isbn = StringField()
    title = StringField('Title')
    authors = FieldList(FormField(PersonForm, default={'role': 'A'}), min_entries=3)
    translators = FieldList(FormField(PersonForm, default={'role': 'T'}), min_entries=3 )
    redactors = FieldList(FormField(PersonForm, default={'role': 'R'}), min_entries=3)
    intro = FieldList(FormField(PersonForm, default={'role': 'I'}), min_entries=3)
    pub_year = StringField('Publication year', validators=[DataRequired()])
    city = StringField('Publication place') # autocomplete z możliwością wpisania 
    city_id_ = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    publisher_name = StringField('Publisher') # autocomplete z możliwością wpisania    
    id_ = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    serie = StringField('Serie') # autocomplete z możliwością wpisania
    serie_id_ = IntegerField('Id', widget=HiddenInput(), validators=[Optional(strip_whitespace=True)])
    origin_language = StringField('Origin language')
    first_edition = StringField('First edition')
#    periodic_num = StringField('Periodic number')
    fiction = SelectField('Fiction', choices=[
                    ('', '---'),
                    (1, 'fiction'),
                    (0, 'non-fiction')
        ], 
        coerce=bool)
    genre = StringField('Genre')
    literary_form = SelectField('Literary form', choices=[
                    ('', '---'),
                    ('PO', 'Poetry'),
                    ('PR', 'Prose'),
                    ('DR', 'Drama')
                ])
#    subject = TextAreaField('Subject')
    precision = TextAreaField('Precision')
    nukat = TextAreaField('NUKAT themes')
    submit = SubmitField('Submit')
    
    class Meta:
        csrf = False


def all_collections():
    return Collection.query.all()


def all_locations():
    return Location.query.all()


class CopyForm(FlaskForm):
    signature_mark = StringField('Singature mark')
    collection = QuerySelectField(query_factory=all_collections, allow_blank=True)
    location = QuerySelectField(query_factory=all_locations, allow_blank=True)
    section = StringField('Section')
    remarques = StringField('Remarques')
    on_shelf = BooleanField('On shelf')
    submit = SubmitField('Submit')
    


class CopyForm2(FlaskForm):
    signature_mark = StringField('Singature mark')
    on_shelf = BooleanField('On shelf')
    section = StringField('Section')
    remarques = StringField('Remarques')
    collection = QuerySelectField(query_factory=all_collections, allow_blank=True)
    location = QuerySelectField(query_factory=all_locations, allow_blank=True)
    
    class Meta:
        csrf = False


class AddBookForm(FlaskForm):
#    title = StringField('Title', render_kw={'readonly': True})
    title = StringField('Title', validators=[DataRequired()] )
    authors = FieldList(FormField(PersonForm, default={'role': 'A'}), min_entries=3)
    translators = FieldList(FormField(PersonForm, default={'role': 'T'}), min_entries=3 )
    redactors = FieldList(FormField(PersonForm, default={'role': 'R'}), min_entries=3)
    intro = FieldList(FormField(PersonForm, default={'role': 'I'}), min_entries=3)
    published = FormField(PublisherForm)
    book = FormField(BookForm)
    copy = FormField(CopyForm2)
    submit = SubmitField('Submit')



