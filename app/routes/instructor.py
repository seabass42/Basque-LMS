from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from app.models import Submission, db

instructor = Blueprint("instructor", __name__)

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
