from app.configurations.database import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    group_id = db.Column(
        db.Integer, db.ForeignKey("groups.id", onupdate="CASCADE", ondelete="CASCADE")
    )

    expenses_list = db.relationship("ExpenseModel", backref="category")
