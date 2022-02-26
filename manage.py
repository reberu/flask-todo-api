#!flask/bin/python
from flask_script import Manager
from project.app import app, db, views

manager = Manager(app)


@manager.command
def create_db():
    """Creates the db tables"""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables"""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
