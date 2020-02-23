from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_script import Manager, Command



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
from server import models
from server import views
migrate = Migrate(app, db)
manager = Manager(app)
CORS(app)

class InitDb(Command):
    def run(self):
        db.create_all()
        return 'success init'

manager.add_command('init_db', InitDb())        