from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from F1DB.f1db import cursor

drivers_dict = {}


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        cursor.execute("select * from users")
        all_users = cursor.fetchall()
        for i in all_users:
            if username.data == i[1]:
                raise ValidationError('This username is already taken! Please choose a different one.')

    def validate_email(self, email):
        cursor.execute("select * from users")
        all_users = cursor.fetchall()
        for i in all_users:
            if email.data == i[2]:
                raise ValidationError('This email is already taken! Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            cursor.execute("select * from users")
            all_users = cursor.fetchall()
            for i in all_users:
                if username.data == i[1]:
                    raise ValidationError('This username is already taken! Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            cursor.execute("select * from users")
            all_users = cursor.fetchall()
            for i in all_users:
                if email.data == i[2]:
                    raise ValidationError('This email is already taken! Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=45)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Post')


class QueryForm(FlaskForm):
    cursor.execute("select year from seasons")
    seasons = cursor.fetchall()
    seasons.sort(key=lambda seasons: seasons, reverse=True)
    sea_r = [("All", "All"), ("Current", "Current")]
    for s in seasons:
        sea_r.append((str(s[0]), str(s[0])))
    cursor.execute("select forename, surname from drivers")
    drivers = cursor.fetchall()
    d_r = [("All", "All")]
    for d in drivers:
        val = (d[0] + " " + d[1])
        d_r.append((val, val))
        drivers_dict[val] = d[0], d[1]
    cursor.execute("select name from constructors")
    constructors = cursor.fetchall()
    con_r = [("All", "All")]
    for c in constructors:
        con_r.append((str(c[0]), str(c[0])))
    cursor.execute("select name from circuits")
    circuits = cursor.fetchall()
    cir_r = [("All", "All")]
    for c in circuits:
        cir_r.append((str(c[0]), str(c[0])))
    cursor.execute("select status from status")
    status = cursor.fetchall()
    status.sort(key=lambda status: status[0][1:-1])
    stat_r = [("All", "All")]
    for s in status:
        stat_r.append((str(s[0]), str(s[0])))

    res_type = SelectField('Season', choices=[("CiI", "Circuit Information"), ("CoI", "Constructor Information"), ("D", "Driver Information"),
                                              ("QR", "Qualifying Results"), ("RR", "Race Results"), ("RS", "Race Schedule"), ("SL", "Season List"), ("FS", "Finishing Status")])
    season = SelectField('Season', choices=sea_r)

    round = SelectField('Round', choices=[])
    driver = SelectField('Driver', choices=d_r)
    constructor = SelectField('Constructor', choices=con_r)
    pos = [("All", "All")]
    for i in range(1, 34):
        pos.append((str(i), str(i)))
    l = [("F", "F"), ("D", "D"), ("N", "N"), ("R", "R"), ("W", "W")]
    pos += l
    fin_pos = SelectField('Finishing Position', choices=pos)
    g_pos = [("All", "All")]
    for i in range(1, 34):
        g_pos.append((str(i), str(i)))
    grid = SelectField('Grid', choices=g_pos)
    f_lap = [("All", "All")]
    for i in range(1, 25):
        f_lap.append((str(i), str(i)))
    fast_lap_rank = SelectField('Fastest Lap Rank', choices=f_lap)
    circuit = SelectField('Circuit', choices=cir_r)
    status = SelectField('Status', choices=stat_r)
    res_per = IntegerField('Results Per Page')
    page = IntegerField('Page')
    submit = SubmitField('Submit')
