from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.users.model import UserModel
    from app.groups.model import GroupModel
    from app.accounts.model import AccountModel
    from app.journal.model import JournalModel
    from app.transactions.model import TransactionModel
    from app.categories.model import CategoryModel
    from app.expenses.model import ExpenseModel
