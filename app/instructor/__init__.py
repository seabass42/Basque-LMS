instructor = Blueprint("instructor", __name__)

@instructor.route("/grade/<int:submission_id>", methods=["GET", "POST"])
@login_required
def grade(submission_id):
    ...
