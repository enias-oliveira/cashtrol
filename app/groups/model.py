from app.configurations.database import db


class GroupModel(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    access_code = db.Column(db.String, nullable=False)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey(
            ("users.id"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    members_list = db.relationship(
        "UserModel", backref="groups_list", secondary="accounts"
    )

    entries_list = db.relationship("JournalModel", backref="group")

    categories_list = db.relationship("CategoryModel", backref="group")
