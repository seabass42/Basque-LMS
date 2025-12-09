import pytest
from app import create_app, db
from app.models import User, Course, Announcement, Assignment, Submission
from datetime import datetime


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def session(app):
    return db.session


def test_create_user(session):
    user = User(email="test@example.com", password="pw123", role="student")
    session.add(user)
    session.commit()

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.role == "student"


def test_create_course(session):
    course = Course(title="CMPE 131")
    session.add(course)
    session.commit()

    assert course.id is not None
    assert course.title == "CMPE 131"


def test_announcement_defaults(session):
    ann = Announcement(
        title="Exam Reminder",
        message="Exam on Friday!"
    )
    session.add(ann)
    session.commit()

    assert ann.id is not None
    assert ann.created_at is not None
    assert isinstance(ann.created_at, datetime)


def test_create_assignment(session):
    due = datetime(2025, 5, 20)
    a = Assignment(title="Homework 1", due_date=due)

    session.add(a)
    session.commit()

    assert a.id is not None
    assert a.due_date == due


def test_submission_relationships(session):
    student = User(email="student@test.com", password="pw", role="student")
    session.add(student)
    session.commit()

    a = Assignment(title="Thisassignment")
    session.add(a)
    session.commit()

    s = Submission(
        student_id=student.id,
        assignment_id=a.id,
        content="My work"
    )
    session.add(s)
    session.commit()

    assert s.id is not None
    assert s.student_id == student.id
    assert s.assignment_id == a.id
    assert s.content == "My work"
    assert s.grade is None