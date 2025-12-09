from datetime import datetime, timedelta
from flask_login import current_user

@app.route("/student")
@login_required
def student_home():
    upcoming = Assignment.query.filter(
        Assignment.due_date >= datetime.now(),
        Assignment.due_date <= datetime.now() + timedelta(days=3)
    ).all()

    return render_template("student_home.html", upcoming=upcoming)
