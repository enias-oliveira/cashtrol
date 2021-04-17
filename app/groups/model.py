from app.configurations.database import db


class GroupModel(db.Model):
    __tablename__ = "groups"
