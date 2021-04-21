from app.configurations.database import db


class JournalModel(db.Model):
    __tablename__ = "journal"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    group_id = db.Column(
        db.Integer,
        db.ForeignKey(
            ("groups.id"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey(
            ("users.id"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    created_at = db.Column(db.DateTime)

    transactions_list = db.relationship("TransactionModel", backref="entry")

    expense = db.relationship("ExpenseModel", uselist=False, backref="entry")

    @classmethod
    def create(cls, name: str, amount: float, group_id: int, created_by: id):
        from flask import current_app

        session = current_app.db.session

        entry = cls(
            name=name,
            amount=amount,
            group_id=group_id,
            created_by=created_by,
        )

        session.add(entry)
        session.commit()

        return entry
