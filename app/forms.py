from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class AnnouncementForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Post Announcement")

class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[Length(max=2000)])
    due_date = DateTimeField('Due date (YYYY-mm-dd HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Create Assignment')

class SubmitAssignmentForm(FlaskForm):
    text_submission = TextAreaField('Type essay/response', validators=[DataRequired()])
    file_submission = FileField('Upload File', validators=[FileAllowed(['pdf', 'docx', 'txt'])])
    submit = SubmitField('Submit Assignment')