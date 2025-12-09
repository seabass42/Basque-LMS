from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Submission, Assignment

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
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
