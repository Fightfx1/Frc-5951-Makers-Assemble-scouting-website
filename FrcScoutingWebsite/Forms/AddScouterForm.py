from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField
from wtforms.validators import DataRequired

class AddMemberToTeam_Form(FlaskForm):
    MemberName = StringField('Add Member Name: ', validators=[DataRequired()])
    submit = SubmitField('Add')