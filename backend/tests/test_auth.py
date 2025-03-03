from flask import session
import app.services.auth as auth
import time

# def test_login(app):
#   with app.test_client:
#     with app.test_request_context():
#       time.sleep(1)
#       response = app.test_client.post(
#         "/api/login",
#         data={"username": "admin", "password": "admin"},
#         headers={'Content-Type': 'application/json'}
#       )
#       print("---->")
#       print("response.json", response.data)
#       # session is still accessible
#       # assert session["user_id"] == 1
#       assert True

#     # session is no longer accessible


def test_get_login_user(app):
  with app.test_request_context():
    # 调用 login_user 函数并传递正确的用户名和密码
    auth.login_user("admin", "admin")
    # 调用 get_login_user 函数
    user_info = auth.get_login_user()

    print("user_info", user_info)

    # 断言返回的用户信息是否正确
    assert user_info["username"] == "admin"
