from app.configurations.database import db

import enum


class TransactionType(enum.Enum):
    debit = "DEBIT"
    credit = "CREDIT"


class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.BigInteger, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum(TransactionType))
    entry_id = db.Column(
        db.Integer,
        db.ForeignKey(
            ("journal.id"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    target_account = db.Column(
        db.Integer,
        db.ForeignKey(
            ("accounts.id"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
