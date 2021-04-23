from app.journal.model import JournalModel
from app.transactions.model import TransactionType


def create_splitted(entry: JournalModel):
    payers_list = [
        {
            "payer_id": transaction.target_user.first().id,
            "paid_amount": transaction.amount,
        }
        for transaction in entry.transactions_list
        if transaction.type == TransactionType.debit
    ]

    benefited_list = [
        {
            "benefited_id": transaction.target_user.first().id,
            "benefited_amount": transaction.amount,
        }
        for transaction in entry.transactions_list
        if transaction.type == TransactionType.credit
    ]

    return {
        "splitted": {
            "payers": payers_list,
            "benefited": benefited_list,
        }
    }


def transaction_serializer(entry: JournalModel):
    splitted = create_splitted(entry)

    return {
        "id": entry.id,
        "name": entry.name,
        "amount": entry.amount,
        "group": entry.group.name,
        "created_at": entry.created_at,
        "created_by": entry.created_by,
        **splitted,
    }
