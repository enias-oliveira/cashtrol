from app.configurations.database import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
