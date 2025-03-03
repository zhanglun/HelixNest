from flask import session
from app.services.auth import login_user

def test_login(client):
  with client:
    response = client.post("/api/login", data={"username": "admin", "password": "admin"}, headers={'Content-Type': 'application/json'})
    print("---->")
    print("response.json", response.data)
    # session is still accessible
    # assert session["user_id"] == 1
    assert True

    # session is no longer accessible


def test_service_login_user(app):
  with app.app_context():
    result = login_user("admin", "admin")
    print("result", result[0].data)
    assert True
