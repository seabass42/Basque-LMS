from flask import (
    render_template,
    Blueprint,
    redirect,
    url_for,
    flash,
    request,
)
from flask_login import current_user, login_required

from app.forms import AnnouncementForm, AssignmentForm
from app.models import Announcement, Assignment, Submission, db

instructor = Blueprint('instructor', __name__, template_folder='templates')


@instructor.route('/')
@login_required
def instructor_home():
    if current_user.role not in ['teacher', 'ta', 'instructor']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    assignments = Assignment.query.order_by(Assignment.due_date.desc()).all()
    
    return render_template('instructor/instructor_template.html',
                           announcements=announcements,
                           assignments=assignments)



@instructor.route('/announcement/create', methods=['GET', 'POST'])
def create_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            message=form.message.data,
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created.', 'success')
        return redirect(url_for('instructor.instructor_home'))

    return render_template('instructor/instructor_create_announcement.html', form=form)


@instructor.route('/submissions')
@login_required
def list_submissions():
    if current_user.role not in ['teacher', 'ta', 'instructor']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    
    submissions = Submission.query.all()
    return render_template('instructor/submissions.html', submissions=submissions)

@instructor.route("/grade/<int:submission_id>", methods=["GET", "POST"])
@login_required
def grade(submission_id):
    if current_user.role not in ['teacher', 'ta', 'instructor']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    submission = Submission.query.get_or_404(submission_id)

    if request.method == "POST":
        new_grade = request.form.get("grade")
        new_feedback = request.form.get("feedback", "").strip()
        
        if new_grade:
            submission.grade = int(new_grade)
        if new_feedback:
            submission.feedback = new_feedback
            
        db.session.commit()
        flash('Grade updated successfully!', 'success')
        return redirect(url_for('instructor.list_submissions'))

    return render_template("instructor/grade.html", submission=submission)


@instructor.route('/assignment/create', methods=['GET', 'POST'])
def create_assignment():
    form = AssignmentForm()

    if form.validate_on_submit():
        assignment = Assignment(
            title=form.title.data,
            due_date=form.due_date.data,
        )
        db.session.add(assignment)
        db.session.commit()
        flash("Assignment created successfully!", "success")
        return redirect(url_for("instructor.instructor_home"))

    return render_template("instructor/instructor_createassignment.html",
                           form=form)


@instructor.route('/assignments')
@login_required
def list_assignments():
    """
    Show all assignments so the instructor can edit or delete them.
    URL: /instructor/assignments
    """
    assignments = Assignment.query.all()
    return render_template('instructor/assignments.html',
                           assignments=assignments)


@instructor.route('/assignments/<int:assignment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_assignment(assignment_id):
    """
    Edit an existing assignment (simple: only title for now).
    """
    assignment = Assignment.query.get_or_404(assignment_id)

    if request.method == 'POST':
        new_title = request.form.get('title', '').strip()

        if not new_title:
            flash('Title is required.', 'danger')
            return redirect(url_for('instructor.edit_assignment',
                                    assignment_id=assignment.id))

        assignment.title = new_title
        db.session.commit()
        flash('Assignment updated.', 'success')
        return redirect(url_for('instructor.list_assignments'))

    return render_template('instructor/edit_assignment.html',
                           assignment=assignment)


@instructor.route('/assignments/<int:assignment_id>/delete', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    """
    Delete an assignment.
    """
    assignment = Assignment.query.get_or_404(assignment_id)

    Submission.query.filter_by(assignment_id=assignment.id).delete()

    db.session.delete(assignment)
    db.session.commit()
    flash('Assignment deleted.', 'info')
    return redirect(url_for('instructor.list_assignments'))


@instructor.route('/submissions/<int:submission_id>/feedback',
                  methods=['GET', 'POST'])
@login_required
def give_feedback(submission_id):
    """
    Instructor can view a submission and add/update feedback.
    URL: /instructor/submissions/<id>/feedback
    """
    submission = Submission.query.get_or_404(submission_id)

    if request.method == 'POST':
        feedback_text = request.form.get('feedback', '').strip()
        submission.feedback = feedback_text or None
        db.session.commit()
        flash('Feedback saved.', 'success')
        return redirect(url_for('instructor.list_assignments'))

    return render_template('instructor/feedback.html',
                           submission=submission)
