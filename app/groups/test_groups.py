from datetime import datetime, date
from pytest import fixture


from app.groups.model import GroupModel
from app.users.model import UserModel
from app.accounts.model import AccountModel
from app.journal.model import JournalModel
from app.transactions.model import TransactionModel, TransactionType
from app.categories.model import CategoryModel
from app.expenses.model import ExpenseModel

from app.app import create_app


@fixture(scope="module")
def app():
    app = create_app()
    app.app_context().push()
    app.db.create_all()

    yield app

    app.db.session.remove()
    app.db.drop_all()


@fixture(scope="module")
def session(app):
    return app.db.session


@fixture(scope="module")
def alice(session):
    alice = UserModel(
        name="Alice",
        email="alice@mail.com",
        password_hash="ajdief",
    )
    session.add(alice)
    session.commit()
    return alice


@fixture(scope="module")
def bob(session):
    bob = UserModel(
        name="bob",
        email="bob@mail.com",
        password_hash="klakdw",
    )
    session.add(bob)
    session.commit()
    return bob


@fixture(scope="module")
def group(session, alice):
    group = GroupModel(
        access_code="123ABC",
        created_by=alice.id,
        name="AP da Galeris",
    )

    session.add(group)
    session.commit()

    return group


@fixture(scope="module")
def group_alice_account(session, alice, group):
    alice_account = AccountModel(user_id=alice.id, group_id=group.id)

    session.add(alice_account)
    session.commit()

    return alice_account


@fixture(scope="module")
def group_bob_account(session, bob, group):
    bob_account = AccountModel(user_id=bob.id, group_id=group.id)

    session.add(bob_account)
    session.commit()

    return bob_account


@fixture(scope="module")
def category_moradia(session, group):
    category = CategoryModel(name="Moradia", group_id=group.id)

    return category


def test_create_payment(
    group: GroupModel,
    alice: UserModel,
    bob: UserModel,
    group_alice_account: AccountModel,
    group_bob_account: AccountModel,
):
    expected_entry_name = "Pagamento"
    expected_entry_amount = 100
    expected_entry_group_id = 1

    expected_transaction_credit_target_account_id = group_alice_account.id
    expected_transaction_debit_target_account_id = group_bob_account.id
    expected_transaction_entry_id = 1

    payment = group.create_payment(
        sender_id=alice.id,
        receiver_id=bob.id,
        amount=100,
    )

    returned_entry: JournalModel = payment["entry"]
    actual_entry: JournalModel = JournalModel.query.get(returned_entry.id)

    returned_credit = payment["transactions"]["credit"]
    actual_credit: TransactionModel = TransactionModel.query.get(returned_credit.id)

    returned_debit = payment["transactions"]["debit"]
    actual_debit: TransactionModel = TransactionModel.query.get(returned_debit.id)

    assert actual_entry.name == expected_entry_name
    assert actual_entry.amount == expected_entry_amount
    assert actual_entry.group_id == expected_entry_group_id

    assert actual_credit.target_account == expected_transaction_credit_target_account_id
    assert actual_credit.entry_id == expected_transaction_entry_id
    assert actual_debit.target_account == expected_transaction_debit_target_account_id
    assert actual_debit.entry_id == expected_transaction_entry_id


def test_create_expense(
    group: GroupModel,
    alice: UserModel,
    bob: UserModel,
    group_alice_account: AccountModel,
    group_bob_account: AccountModel,
    session,
    category_moradia,
):

    charlie = UserModel(
        name="Charlie",
        email="charlie@mail.com",
        password_hash="kklafeasflmrwegko",
    )

    session.add(charlie)
    session.commit()

    group_charlie_account = AccountModel(user_id=charlie.id, group_id=group.id)

    session.add(group_charlie_account)
    session.commit()

    given_splitted = {
        "payers": [{"payer_id": alice.id, "paid_amount": 100}],
        "benefited": [
            {"benefited_id": alice.id, "benefited_amount": 40},
            {"benefited_id": bob.id, "benefited_amount": 30},
            {"benefited_id": charlie.id, "benefited_amount": 30},
        ],
    }

    expected_entry_name = "Conta Luz"
    expected_entry_amount = 100
    expected_entry_group_id = 1
    expected_entry_created_by = alice.id
    expected_entry_created_at = datetime.combine(date.today(), datetime.min.time())

    expected_transactions_debit_target_account_id = [group_alice_account.id]
    expected_transactions_credit_target_account_id = [
        group_alice_account.id,
        group_bob_account.id,
        group_charlie_account.id,
    ]
    expected_transactions_entries_id = [2, 2, 2, 2]

    expected_expense_id = 1
    expected_expense_category_id = category_moradia.id
    expected_expense_description = "Veio mais alta por causa da secadora"
    expected_expense_journal_id = 2

    expense_entry: JournalModel = group.create_expense(
        name="Conta Luz",
        amount=100,
        created_by=alice.id,
        splitted=given_splitted,
        category_id=category_moradia.id,
        description=expected_expense_description,
    )

    actual_entry: JournalModel = JournalModel.query.get(expense_entry.id)

    actual_transactions_credit: list[
        TransactionModel
    ] = TransactionModel.query.filter_by(
        type=TransactionType.credit, entry_id=actual_entry.id
    ).all()

    actual_transactions_credit_target_account_id = [
        transaction.target_account for transaction in actual_transactions_credit
    ]

    actual_transactions_debit: list[
        TransactionModel
    ] = TransactionModel.query.filter_by(
        type=TransactionType.debit, entry_id=actual_entry.id
    ).all()

    actual_transactions_debit_target_account_id = [
        transaction.target_account for transaction in actual_transactions_debit
    ]

    actual_all_transactions = actual_transactions_credit + actual_transactions_debit

    actual_transactions_entries_id = [
        transaction.entry_id for transaction in actual_all_transactions
    ]

    actual_expense = ExpenseModel.query.filter_by(journal_id=actual_entry.id).first()

    assert actual_entry.name == expected_entry_name
    assert actual_entry.amount == expected_entry_amount
    assert actual_entry.group_id == expected_entry_group_id
    assert actual_entry.created_by == expected_entry_created_by
    assert actual_entry.created_at == expected_entry_created_at
    assert actual_transactions_entries_id == expected_transactions_entries_id

    assert actual_expense.id == expected_expense_id
    assert actual_expense.category_id == expected_expense_category_id
    assert actual_expense.description == expected_expense_description
    assert actual_expense.journal_id == expected_expense_journal_id

    assert (
        actual_transactions_credit_target_account_id
        == expected_transactions_credit_target_account_id
    )
    assert (
        actual_transactions_debit_target_account_id
        == expected_transactions_debit_target_account_id
    )


def test_get_balance(group: GroupModel):
    expected = {
        "balance": [
            {"user_id": 1, "user_saldo": 160.00},
            {"user_id": 2, "user_saldo": -130.00},
            {"user_id": 3, "user_saldo": -30.00},
        ]
    }

    actual = group.get_balance()

    assert actual == expected
