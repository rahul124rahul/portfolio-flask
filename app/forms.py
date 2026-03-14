from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=200)])
    subject = StringField("Subject", validators=[Optional(), Length(max=200)])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")


class ProfileForm(FlaskForm):
    name = StringField("Name", validators=[Optional(), Length(max=100)])
    title = StringField("Title", validators=[Optional(), Length(max=150)])
    tagline = StringField("Tagline", validators=[Optional(), Length(max=200)])
    bio = TextAreaField("Bio", validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Length(max=120)])
    phone = StringField("Phone", validators=[Optional(), Length(max=50)])
    location = StringField("Location", validators=[Optional(), Length(max=150)])
    submit = SubmitField("Save Profile")


class ProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[DataRequired()])
    github = StringField("GitHub URL", validators=[Optional(), Length(max=200)])
    demo = StringField("Demo URL", validators=[Optional(), Length(max=200)])
    submit = SubmitField("Save Project")


class SkillForm(FlaskForm):
    name = StringField("Skill Name", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Add Skill")


class ExperienceForm(FlaskForm):
    role = StringField("Role", validators=[DataRequired(), Length(max=150)])
    company = StringField("Company", validators=[DataRequired(), Length(max=150)])
    company_url = StringField("Company Website", validators=[Optional(), Length(max=200)])
    location = StringField("Location", validators=[Optional(), Length(max=150)])
    start_date = StringField("Start Date", validators=[Optional(), Length(max=50)])
    end_date = StringField("End Date", validators=[Optional(), Length(max=50)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Save Experience")


class SocialLinkForm(FlaskForm):
    name = StringField("Platform", validators=[DataRequired(), Length(max=100)])
    url = StringField("URL", validators=[DataRequired(), Length(max=300)])
    icon = StringField("Icon Class", validators=[Optional(), Length(max=100)])
    submit = SubmitField("Add Social Link")
