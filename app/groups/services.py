import string
import random

from .model import TransactionModel, TransactionType


def create_invitation_code():
    letters = string.ascii_uppercase + string.digits
    random_letters = "".join(random.choice(letters) for i in range(6))

    return random_letters


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
