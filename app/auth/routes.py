from flask import render_template, Blueprint, redirect, url_for, flash, request
from app.forms import LoginForm


auth = Blueprint('auth', __name__, template_folder ='templates')


# http://127.0.0.1:5000

@auth.route('/login', methods =['GET'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

@auth.route('/login', methods = ["POST"])
def login_post():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Not implemented', 'info')
        return redirect(url_for('auth.login'))

    flash('Invalid form data', 'danger')
    return redirect(url_for('auth.login'))
            


