from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Submission, Assignment

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role in ['teacher', 'ta', 'instructor']:
            return redirect(url_for('instructor.instructor_home'))
        elif current_user.role == 'student':
            return redirect(url_for('student.student_home'))
    return render_template('main/index.html')

@main.route('/feature')
def feature():
    return render_template('main/feature.html')

@main.route('/grades')
@login_required
def view_grades():
    """
    Students can view their grades for all submissions.
    Shows assignment title, grade, and feedback.
    """
    submissions = Submission.query.filter_by(student_id=current_user.id).all()
    return render_template('main/grades.html', submissions=submissions)
