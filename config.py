import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "chave-secreta-segura"
    SQLALCHEMY_DATABASE_URI = "sqlite:///money_mate.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
