from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = StringField("Team Leader id", validators=[DataRequired()])
    job = StringField("Job Title", validators=[DataRequired()])
    work_size = StringField("Work Size", validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Add job')
