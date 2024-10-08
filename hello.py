from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
boostrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'the real secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    error = ""
    if form.validate_on_submit():
        # First validate the email address is a UofT email
        if not (form.email.data.endswith('@mail.utoronto.ca')) or (form.email.data.endswith('@utoronto.ca')):
            flash('Please use your UofT email address')
            error = "Please use your UofT email address"
            return render_template('index.html',
        form = NameForm(), name = session.get('name'), email = session.get('email'),error = error)

        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html',
        form = form, name = session.get('name'), email = session.get('email'),error = error)


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT email?', validators=[DataRequired()])
    submit = SubmitField('Submit')



if __name__ == '__main__':
    # run the app on port 5001
    app.run(host='0.0.0.0', port=5000)