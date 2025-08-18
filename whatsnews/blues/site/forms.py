# /whatsnews/blues/site/forms


from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, SelectMultipleField, StringField
from wtforms.validators import DataRequired, URL


class SiteForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    name_en = StringField('Name (EN)')
    name_sort = StringField('Name (sort)', validators=[DataRequired()])
    url = StringField('Site URL', validators=[DataRequired(), URL()])
    feed_url = StringField('Feed URL', validators=[DataRequired(), URL()])
    country = StringField('Country', validators=[DataRequired()])
    active = BooleanField('Active')