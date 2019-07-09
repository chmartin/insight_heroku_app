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
from get_stats import get_stats

class ExampleForm(Form):
    steamid = IntegerField(' ', description='This is the steamid of user to be considered.')

    submit_button = SubmitField('Load Analysis')


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
        churn_stats = []
        if request.method == "POST":
            #get steamid that the user has entered
            steamid_to_process = request.form['steamid']
            churn_stats = get_stats(steamid_to_process)

        #print(churn_stats)
        return render_template('index.html', form=form, churn_stats=[churn_stats])
    
    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('cover.html')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
else:
    gunicorn_app = create_app()
