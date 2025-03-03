import pytest
from flask import session
from app import create_app

@pytest.fixture()
def app():
  my_app = create_app()
  my_app.config.update({
    "TESTING": True,
  })

  yield my_app

@pytest.fixture()
def client(app):
  return app.test_client()

@pytest.fixture()
def runner(app):
  return app.test_cli_runner()

