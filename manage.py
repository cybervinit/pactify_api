import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app
from main.models import db

app.config.from_object(os.getenv('PACTIFY_API_CONFIG_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
