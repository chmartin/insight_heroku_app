# This is modified from: https://gist.github.com/ericbarnhill/251df20105991674c701d33d65437a50 
# and https://github.com/mbr/flask-bootstrap/blob/master/sample_application/ 

from flask import Flask, request, render_template, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from get_digits import get_digits

class ExampleForm(Form):
    steamid = IntegerField('Enter Steamid of User in Question.', description='This is the steamid of user to be considered.')

    submit_button = SubmitField('Submit Form')


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=('GET', 'POST'))
    def index():
        form = ExampleForm()
        form.validate_on_submit()  # to get error messages to the browser
        flash('critical message', 'critical')
        flash('error message', 'error')
        flash('warning message', 'warning')
        flash('info message', 'info')
        flash('debug message', 'debug')
        flash('different message', 'different')
        flash('uncategorized message')
        letters = []
        if request.method == "POST":
            #get steamid that the user has entered
            steamid_to_process = request.form['steamid']
            letters = get_digits(steamid_to_process)

        return render_template('index.html', form=form, letters=letters)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
