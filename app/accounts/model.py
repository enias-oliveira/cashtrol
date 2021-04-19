from app.configurations.database import db


class AccountModel(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.BigInteger, primary_key=True)
    group_id = db.Column(
        db.Integer, db.ForeignKey("groups.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE")
    )
