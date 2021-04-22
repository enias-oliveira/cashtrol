from app.configurations.database import db


class ExpenseModel(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String)
    journal_id = db.Column(
        db.Integer,
        db.ForeignKey(
            ("journal.id"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey(
            ("categories.id"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    @classmethod
    def create(cls, description: str, journal_id: int, category_id: int):
        expense = cls(
            description=description,
            journal_id=journal_id,
            category_id=category_id,
        )

        from flask import current_app

        session = current_app.db.session

        session.add(expense)
        session.commit()

        return expense
