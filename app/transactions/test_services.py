from pytest import fixture

from app.groups.model import GroupModel
from app.users.model import UserModel
from app.accounts.model import AccountModel
from app.journal.model import JournalModel

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
def charlie(session):
    charlie = UserModel(
        name="charlie",
        email="charlie@mail.com",
        password_hash="klakdw",
    )
    session.add(charlie)
    session.commit()
    return charlie


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
def group_charlie_account(session, charlie, group):
    charlie_account = AccountModel(user_id=charlie.id, group_id=group.id)

    session.add(charlie_account)
    session.commit()

    return charlie_account


def test_create_splitted(
    group: GroupModel,
    alice: UserModel,
    bob: UserModel,
    charlie: UserModel,
    group_alice_account,
    group_bob_account,
    group_charlie_account,
):
    given_splitted = {
        "payers": [{"payer_id": alice.id, "paid_amount": 100.00}],
        "benefited": [
            {"benefited_id": alice.id, "benefited_amount": 40.00},
            {"benefited_id": bob.id, "benefited_amount": 30.00},
            {"benefited_id": charlie.id, "benefited_amount": 30.00},
        ],
    }

    expected = {"splitted": given_splitted}

    expense = group.create_expense(
        name="Conta Luz",
        amount=100,
        created_by=alice.id,
        splitted=given_splitted,
        description="Veio mais alta por causa da secadora",
    )

    from .services import create_splitted

    actual = create_splitted(expense)

    assert actual == expected


def test_transaction_serializer(
    group: GroupModel,
    alice: UserModel,
    bob: UserModel,
    charlie: UserModel,
    group_alice_account,
    group_bob_account,
    group_charlie_account,
):

    from datetime import date, datetime

    expected = {
        "id": 1,
        "name": "Conta Luz",
        "amount": 100.00,
        "group": "AP da Galeris",
        "created_at": datetime.combine(date.today(), datetime.min.time()),
        "created_by": alice.id,
        "splitted": {
            "payers": [{"payer_id": alice.id, "paid_amount": 100.00}],
            "benefited": [
                {"benefited_id": alice.id, "benefited_amount": 40.00},
                {"benefited_id": bob.id, "benefited_amount": 30.00},
                {"benefited_id": charlie.id, "benefited_amount": 30.00},
            ],
        },
    }

    expense = JournalModel.query.get(1)

    from .services import transaction_serializer

    actual = transaction_serializer(expense)

    assert actual == expected
