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

    target_user = db.relationship(
        "UserModel",
        backref="transactions_list",
        secondary="accounts",
        viewonly=True,
    )

    group = db.relationship(
        "GroupModel",
        backref="transactions_list",
        secondary="accounts",
        viewonly=True,
    )

    @classmethod
    def create(
        cls,
        amount: int,
        type: TransactionType,
        entry_id: int,
        target_account: int,
    ):
        from flask import current_app

        session = current_app.db.session

        transaction = cls(
            amount=amount,
            type=type,
            entry_id=entry_id,
            target_account=target_account,
        )

        session.add(transaction)
        session.commit()

        return transaction
