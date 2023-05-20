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
    
class BookSeatForm(FlaskForm):
    seat_1 = StringField(validators=[DataRequired()])
    seat_2 = StringField(validators=[DataRequired()])
    seat_3 = StringField(validators=[DataRequired()])
    seat_4 = StringField(validators=[DataRequired()])
    seat_5 = StringField(validators=[DataRequired()])
    seat_6 = StringField(validators=[DataRequired()])
    seat_7 = StringField(validators=[DataRequired()])
    seat_8 = StringField(validators=[DataRequired()])
    seat_9 = StringField(validators=[DataRequired()])
    seat_10 = StringField(validators=[DataRequired()])
    seat_11 = StringField(validators=[DataRequired()])
    seat_12 = StringField(validators=[DataRequired()])
    seat_13 = StringField(validators=[DataRequired()])
    seat_14 = StringField(validators=[DataRequired()])
    seat_15 = StringField(validators=[DataRequired()])
    seat_16 = StringField(validators=[DataRequired()])
    seat_17 = StringField(validators=[DataRequired()])
    seat_18 = StringField(validators=[DataRequired()])
    seat_19 = StringField(validators=[DataRequired()])
    seat_20 = StringField(validators=[DataRequired()])
    seat_21 = StringField(validators=[DataRequired()])
    seat_22 = StringField(validators=[DataRequired()])
    seat_23 = StringField(validators=[DataRequired()])
    seat_24 = StringField(validators=[DataRequired()])
    seat_25 = StringField(validators=[DataRequired()])
    seat_26 = StringField(validators=[DataRequired()])
    seat_27 = StringField(validators=[DataRequired()])
    seat_28 = StringField(validators=[DataRequired()])
    seat_29 = StringField(validators=[DataRequired()])
    seat_30 = StringField(validators=[DataRequired()])
    seat_31 = StringField(validators=[DataRequired()])
    seat_32 = StringField(validators=[DataRequired()])
    seat_33 = StringField(validators=[DataRequired()])
    seat_34 = StringField(validators=[DataRequired()])
    seat_35 = StringField(validators=[DataRequired()])
    seat_36 = StringField(validators=[DataRequired()])
    seat_37 = StringField(validators=[DataRequired()])
    seat_38 = StringField(validators=[DataRequired()])
    seat_39 = StringField(validators=[DataRequired()])
    seat_40 = StringField(validators=[DataRequired()])
    seat_41 = StringField(validators=[DataRequired()])
    seat_42 = StringField(validators=[DataRequired()])
    seat_43 = StringField(validators=[DataRequired()])
    seat_44 = StringField(validators=[DataRequired()])
    seat_45 = StringField(validators=[DataRequired()])
    seat_46 = StringField(validators=[DataRequired()])
    seat_47 = StringField(validators=[DataRequired()])
    seat_48 = StringField(validators=[DataRequired()])
    seat_49 = StringField(validators=[DataRequired()])
    seat_50 = StringField(validators=[DataRequired()])
    seat_51 = StringField(validators=[DataRequired()])
    seat_52 = StringField(validators=[DataRequired()])
    seat_53 = StringField(validators=[DataRequired()])
    seat_54 = StringField(validators=[DataRequired()])
    seat_55 = StringField(validators=[DataRequired()])
    seat_56 = StringField(validators=[DataRequired()])
    seat_57 = StringField(validators=[DataRequired()])
    seat_58 = StringField(validators=[DataRequired()])
    seat_59 = StringField(validators=[DataRequired()])
    seat_60 = StringField(validators=[DataRequired()])
    seat_61 = StringField(validators=[DataRequired()])
    seat_62 = StringField(validators=[DataRequired()])
    seat_63 = StringField(validators=[DataRequired()])
    seat_64 = StringField(validators=[DataRequired()])
    seat_65 = StringField(validators=[DataRequired()])
    seat_66 = StringField(validators=[DataRequired()])
    seat_67 = StringField(validators=[DataRequired()])
    seat_68 = StringField(validators=[DataRequired()])
    seat_69 = StringField(validators=[DataRequired()])
    seat_70 = StringField(validators=[DataRequired()])
    seat_71 = StringField(validators=[DataRequired()])
    seat_72 = StringField(validators=[DataRequired()])
    seat_73 = StringField(validators=[DataRequired()])
    seat_74 = StringField(validators=[DataRequired()])
    seat_75 = StringField(validators=[DataRequired()])
    seat_76 = StringField(validators=[DataRequired()])
    seat_77 = StringField(validators=[DataRequired()])
    seat_78 = StringField(validators=[DataRequired()])
    seat_79 = StringField(validators=[DataRequired()])
    seat_80 = StringField(validators=[DataRequired()])
    seat_81 = StringField(validators=[DataRequired()])
    seat_82 = StringField(validators=[DataRequired()])
    seat_83 = StringField(validators=[DataRequired()])
    seat_84 = StringField(validators=[DataRequired()])
    seat_85 = StringField(validators=[DataRequired()])
    seat_86 = StringField(validators=[DataRequired()])
    seat_87 = StringField(validators=[DataRequired()])
    seat_88 = StringField(validators=[DataRequired()])
    seat_89 = StringField(validators=[DataRequired()])
    seat_90 = StringField(validators=[DataRequired()])
    seat_91 = StringField(validators=[DataRequired()])
    seat_92 = StringField(validators=[DataRequired()])
    seat_93 = StringField(validators=[DataRequired()])
    seat_94 = StringField(validators=[DataRequired()])
    seat_95 = StringField(validators=[DataRequired()])
    seat_96 = StringField(validators=[DataRequired()])
    seat_97 = StringField(validators=[DataRequired()])
    seat_98 = StringField(validators=[DataRequired()])
    seat_99 = StringField(validators=[DataRequired()])
    seat_100 = StringField(validators=[DataRequired()])
    submit = SubmitField('Select seats')