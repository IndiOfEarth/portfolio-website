from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


class AuthenticationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Enter")

class ImageForm(FlaskForm):
    path = SelectField("File destination", choices=[('other-imgs','other(art/photography, etc...)'), ('standard','standard(tech-projects, uni-projects)')])
    file = FileField('File')
    submit = SubmitField("Enter")

class ProjectForm(FlaskForm):
    id = StringField("ID", validators=[DataRequired()])
    project_name = StringField("Name of Project", validators=[DataRequired()])
    project_type = StringField("Type of Project", validators=[DataRequired()])
    short_desc = StringField("Short Description about Project", widget=TextArea(), validators=[DataRequired()])
    description = StringField("Long Description about Project", widget=TextArea(), validators=[DataRequired()])
    img_url_1 = StringField("Img_URL_1 (write filename)", validators=[DataRequired()])
    img_url_2 = StringField("Img_URL_2 (write filename)", validators=[DataRequired()])
    img_url_3 = StringField("Img_URL_3 (write filename)", validators=[DataRequired()])
    img_url_4 = StringField("Img_URL_4 (write filename)", validators=[DataRequired()])
    modal_id = StringField("Modal ID", validators=[DataRequired()])
    submit = SubmitField("Enter")

