from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    EventCode = StringField('Event Code:',validators=[DataRequired()])
    Season = StringField('Season:',validators=[DataRequired()])
    tournamentLevel = SelectField('Tournament Level:',choices=[("qual","qualification matches"),("playoff","finals matches")],validators=[DataRequired])
    submit = SubmitField('Save')