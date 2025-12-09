from flask import render_template, Blueprint, redirect, url_for, flash, request
from app.forms import AnnouncementForm
from flask_login import current_user
from app.models import Announcement

instructor = Blueprint('instructor', __name__, template_folder='templates')

# http://127.0.0.1:5000

@instructor.route('/')
def instructor_home():
    return render_template('instructor/instructor_template.html', users=current_user)

@instructor.route('/announcement/create', methods=['GET', 'POST'])
def create_announcement():
    form = AnnouncementForm()

    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            message=form.message.data,
        )

