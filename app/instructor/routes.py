from flask import render_template, Blueprint, redirect, url_for, flash, request
from app.forms import AnnouncementForm
from flask_login import current_user, login_required
from app.models import Announcement, Submission, db

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
@instructor.route("/grade/<int:submission_id>", methods=["GET", "POST"])
@login_required
def grade(submission_id):
    if current_user.role != "instructor":
        return "Unauthorized", 403

    submission = Submission.query.get(submission_id)

    if request.method == "POST":
        new_grade = request.form.get("grade")
        submission.grade = int(new_grade)
        db.session.commit()
        return redirect("/instructor/submissions")

    return render_template("grade.html", submission=submission)

