from .model import TransactionModel, TransactionType


def get_invitation_code(data):
    return data["invite_code"]


def create_member_balance(member_id, transactions_list: list[TransactionModel]):
    debit_transactions = [
        transaction.amount
        for transaction in transactions_list
        if transaction.type == TransactionType.debit
    ]
    debit_total = sum(debit_transactions)

    credit_transactions = [
        transaction.amount
        for transaction in transactions_list
        if transaction.type == TransactionType.credit
    ]
    credit_total = sum(credit_transactions)

    member_saldo = debit_total - credit_total

    return {"user_id": member_id, "user_saldo": member_saldo}
