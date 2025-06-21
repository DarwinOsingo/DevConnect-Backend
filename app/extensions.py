from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Initialize extensions without app
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
