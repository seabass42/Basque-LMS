from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from app import db
from app.models import Assignment, Submission
from app.forms import SubmitAssignmentForm

student = Blueprint('student', __name__, template_folder='templates')

@student.route('/assignment/<int:assignment_id>/submit', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    if current_user.role != "student":
        abort(403)

    assignment = Assignment.query.get_or_404(assignment_id)
    form = SubmitAssignmentForm()

    if form.validate_on_submit():
        filename = None

        # if file was uploaded
        if form.file_submission.data:
            file = form.file_submission.data
            filename = secure_filename(file.filename)
            upload_path = os.path.join('app', 'static', 'uploads', filename)
            file.save(upload_path)

        submission = Submission(
            assignment_id=assignment.id,
            student_id=current_user.id,
            text=form.text_submission.data,
            file_path=filename
        )

        db.session.add(submission)
        db.session.commit()

        flash("Assignment submitted!", "success")
        return redirect(url_for('student.student_home'))

    return render_template('student/submit_assignment.html', form=form, assignment=assignment)