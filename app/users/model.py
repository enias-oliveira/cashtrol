from app.configurations.database import db


class UserModel(db.Model):
    __tablename__ = "users"
