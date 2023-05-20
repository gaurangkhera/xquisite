from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Login")

class RegForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Length(min=4, max=64)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32)])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField("Register")

class PredictForm(FlaskForm):
    team1 = StringField(validators=[DataRequired()])
    team2 = StringField(validators=[DataRequired()])
    toss_winner = StringField(validators=[DataRequired()])
    submit = SubmitField('Predict winner!')