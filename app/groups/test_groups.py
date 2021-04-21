from pytest import fixture

from app.groups.model import GroupModel
from app.users.model import UserModel
from app.accounts.model import AccountModel
from app.journal.model import JournalModel
from app.transactions.model import TransactionModel

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
