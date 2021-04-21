from app.configurations.database import db
from app.users.model import UserModel
from app.accounts.model import AccountModel
from app.journal.model import JournalModel
from app.transactions.model import TransactionModel, TransactionType


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

    def is_member(self, user_id: int) -> int:
        members_id = [member.id for member in self.members_list]
        return user_id in members_id

    def are_members(self, users_id: list) -> bool:
        return all([self.is_member(user_id) for user_id in users_id])

    def create_payment(self, sender_id: int, receiver_id: int, amount: float) -> dict:
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

        payment_entry: JournalModel = JournalModel.create(
            name="Pagamento",
            amount=amount,
            group_id=self.id,
            created_by=receiver_id,
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
