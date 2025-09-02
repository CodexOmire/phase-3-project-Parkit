import os
import tempfile

import click
from click.testing import CliRunner

from app import create_app
from db import db
from models import User
from cli import cli


def setup_app_for_test():
    app = create_app()
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()
    return app


def test_user_model_creation():
    app = setup_app_for_test()
    with app.app_context():
        user = User(name="Test", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        assert user.id is not None


def test_cli_db_create_and_create_user():
    app = setup_app_for_test()
    runner = CliRunner()
    # create tables via CLI first to simulate real usage
    result_create = runner.invoke(cli, ["db-create"])
    assert result_create.exit_code == 0
    result = runner.invoke(cli, ["create-user"], input="Test User\ntest2@example.com\n")
    assert result.exit_code == 0
    assert "Created user id=" in result.output

