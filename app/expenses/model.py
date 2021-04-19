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
