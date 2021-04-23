from app.configurations.database import db
from app.accounts.model import AccountModel
from app.journal.model import JournalModel
from app.transactions.model import TransactionModel, TransactionType
from app.expenses.model import ExpenseModel

from datetime import date


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

    def __repr__(self):
        return f'<Grupo {self.name} -- Feito por id->{self.created_by}>'

    def is_member(self, user_id: int) -> int:
        members_id = [member.id for member in self.members_list]
        return user_id in members_id

    def are_members(self, users_id: list) -> bool:
        return all([self.is_member(user_id) for user_id in users_id])

    def create_payment(self, sender_id: int, receiver_id: int, amount: float):
        if not self.are_members([sender_id, receiver_id]):
            raise ValueError("Not all users are group members.")

        sender_account = AccountModel.query.filter_by(
            user_id=sender_id,
            group_id=self.id,
        ).first()

        receiver_account = AccountModel.query.filter_by(
            user_id=receiver_id,
            group_id=self.id,
        ).first()

        from datetime import date

        payment_entry: JournalModel = JournalModel.create(
            name="Pagamento",
            amount=amount,
            group_id=self.id,
            created_by=receiver_id,
            created_at=date.today(),
        )

        sender_transaction: TransactionModel = TransactionModel.create(
            amount=100,
            type=TransactionType.credit,
            entry_id=payment_entry.id,
            target_account=sender_account.id,
        )

        receiver_transaction: TransactionModel = TransactionModel.create(
            amount=100,
            type=TransactionType.credit,
            entry_id=payment_entry.id,
            target_account=receiver_account.id,
        )

        return {
            "entry": payment_entry,
            "transactions": {
                "credit": sender_transaction,
                "debit": receiver_transaction,
            },
        }

    def create_expense(
        self,
        name: str,
        amount: id,
        created_by: id,
        splitted: dict,
        category_id: int = None,
        description: str = "",
    ):
        payers = splitted["payers"]
        benefited = splitted["benefited"]

        payers_id = [payer["payer_id"] for payer in payers]
        benefited_id = [benefiter["benefited_id"] for benefiter in benefited]

        if not self.are_members(payers_id + benefited_id):
            raise ValueError("Not all users are group members.")

        payers_amount = [payer["paid_amount"] for payer in payers]
        benefited_amount = [benefiter["benefited_amount"] for benefiter in benefited]

        from functools import reduce

        payers_total = reduce(lambda acc, cur: acc + cur, payers_amount)
        benefited_total = reduce(lambda acc, cur: acc + cur, benefited_amount)

        if not amount == benefited_total == payers_total:
            raise ValueError("Amount Splitted is diferent from Expense amount.")

        expense_entry = JournalModel.create(
            name=name,
            amount=amount,
            group_id=self.id,
            created_by=created_by,
            created_at=date.today(),
        )

        for payer in payers:
            payer_account = AccountModel.query.filter_by(
                user_id=payer["payer_id"], group_id=self.id
            ).first()

            TransactionModel.create(
                amount=payer["paid_amount"],
                type=TransactionType.debit,
                entry_id=expense_entry.id,
                target_account=payer_account.id,
            )

        for benefiter in benefited:
            benefiter_account = AccountModel.query.filter_by(
                user_id=benefiter["benefited_id"], group_id=self.id
            ).first()

            TransactionModel.create(
                amount=benefiter["benefited_amount"],
                type=TransactionType.credit,
                entry_id=expense_entry.id,
                target_account=benefiter_account.id,
            )

        expense = ExpenseModel.create(
            description=description,
            journal_id=expense_entry.id,
            category_id=category_id,
        )

        return expense_entry
