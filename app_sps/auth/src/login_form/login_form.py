from flask import session
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from app_sps.locales.load_language import load_language

class LoginForm(FlaskForm):
    """
    Login form for user authentication with localization support.

    Attributes:
        mail (StringField): Email input field with email format validation.
        psw (PasswordField): Password input field with required length validation (4-35 characters).
        remember_me (BooleanField): Checkbox to remember the user for future sessions.
        submit (SubmitField): Submit button for the form.

    Methods:
        __init__(*args, **kwargs): Initializes the form and sets localized labels
                                   based on the current session language. Defaults
                                   to English if localization fails.
    """
    mail = StringField(validators=[Email()])
    psw = PasswordField(validators=[DataRequired(), Length(min=4, max=35)])
    remember_me = BooleanField(default=False)
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            lang = session.get('language', 'en')
            content = load_language(lang)
            labels = content['login']['labels']
        except Exception:
            labels = ['Email', 'Password', 'Remember me', 'Sign in']

        self.mail.label.text = f"{labels[0]}: "
        self.psw.label.text = f"{labels[1]}: "
        self.remember_me.label.text = f"{labels[2]}"
        self.submit.label.text = f"{labels[3]} "
