from apps.personal_website.requests import app  # pylint: disable=import-error, useless-option-value, nknown-option-value, unrecognized-option


def test_get_home():
    response = app.test_client().get("/")

    assert response.status_code == 200


def test_get_projects():
    response = app.test_client().get("/projects")

    assert response.status_code == 200


def test_get_skills():
    response = app.test_client().get("/skills")

    assert response.status_code == 200


def test_get_education():
    response = app.test_client().get("/education")

    assert response.status_code == 200


def test_get_resume():
    response = app.test_client().get("/resume")

    assert response.status_code == 200
    

def test_get_robots_txt():
    response = app.test_client().get("/robots.txt")

    assert response.status_code == 200
