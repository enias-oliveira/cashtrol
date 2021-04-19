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

    transactions_list = db.relationship("TransactionModel", backref="entry")
