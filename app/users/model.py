from app.configurations.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    def validate_password(self, given_password: str) -> bool:
        return check_password_hash(self.password_hash, given_password)

    @property
    def password(self) -> None:
        raise NotImplementedError("Password is not accessible")

    @password.setter
    def password(self, new_password: str) -> None:
        self.password_hash = generate_password_hash(new_password)
