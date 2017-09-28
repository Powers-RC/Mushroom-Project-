from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import Length, InputRequired

class feature_string(FlaskForm):
    """
    Creates form to submit mushroom attributes and for the agreement that the results are in no way definative.
    """
    agreement = BooleanField("Agreement Box", validators=[InputRequired()])
