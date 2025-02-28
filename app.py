from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

csrf = CSRFProtect(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from controllers.auth import auth_bp
from controllers.expenses import expenses_bp
from controllers.reports import reports_bp
from controllers.main import main_bp
from controllers.budgets import budgets_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(expenses_bp, url_prefix="/expenses")
app.register_blueprint(reports_bp, url_prefix="/reports")
app.register_blueprint(main_bp)
app.register_blueprint(budgets_bp, url_prefix="/budgets") 

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
