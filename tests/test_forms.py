from app.forms import LoginForm, AnnouncementForm

def test_login_form_valid(app):
    with app.test_request_context(method='POST'):
        form = LoginForm(
            username="thisusername",
            password="123",
            remember_me=True
        )
        assert form.validate() is True
        assert form.username.data == "thisusername"
        assert form.password.data == "123"
        assert form.remember_me.data is True


def test_login_form_missing_username(app):
    with app.test_request_context(method='POST'):
        form = LoginForm(
            username="",  # missing
            password="something"
        )
        assert form.validate() is False
        assert "This field is required." in form.username.errors


def test_login_form_fields_exist():
    form = LoginForm()
    assert hasattr(form, "username")
    assert hasattr(form, "password")
    assert hasattr(form, "remember_me")
    assert hasattr(form, "submit")