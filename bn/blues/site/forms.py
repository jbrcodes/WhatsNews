# /bn/blues/site/forms


from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, SelectMultipleField, StringField
from wtforms.validators import DataRequired, URL


class SiteForm(FlaskForm):
    slug = StringField('Slug', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    name_en = StringField('Name (EN)')
    name_sort = StringField('Name (sort)', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    language = StringField('Language', validators=[DataRequired()])
    url = StringField('Site URL', validators=[DataRequired(), URL()])
    fetch_type = StringField('Fetch Type', validators=[DataRequired()])
    fetch_url = StringField('Fetch URL', validators=[DataRequired(), URL()])
    scraper_class_name = StringField('Scraper Class Name')
    lang_src = StringField('Source Language', validators=[DataRequired()])
    lang_dest = StringField('Destination Language', validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)