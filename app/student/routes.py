from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from app import db
from app.models import Assignment, Submission
from app.forms import SubmitAssignmentForm

student = Blueprint('student', __name__, template_folder='templates')

@student.route('/')
@login_required
def student_home():
    from datetime import datetime, timedelta
    
    now = datetime.utcnow()
    upcoming_deadline = now + timedelta(days=7)
    
    upcoming_assignments = Assignment.query.filter(
        Assignment.due_date >= now,
        Assignment.due_date <= upcoming_deadline
    ).order_by(Assignment.due_date).all()
    
    all_assignments = Assignment.query.filter(Assignment.due_date >= now).order_by(Assignment.due_date).all()
    
    my_submissions = Submission.query.filter_by(student_id=current_user.id).all()
    submitted_ids = [s.assignment_id for s in my_submissions]
    
    return render_template('student/student_page_template.html', 
                          upcoming_assignments=upcoming_assignments,
                          all_assignments=all_assignments,
                          my_submissions=my_submissions,
                          submitted_ids=submitted_ids,
                          now=now)
    
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
