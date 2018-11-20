from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps.models import db
from werkzeug import local
from flask import Flask

from apps import create_app
from flask import g,current_app

app = create_app()
Migrate(app, db)
manager = Manager(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run()
    print(app.url_map)
    manager.run()
