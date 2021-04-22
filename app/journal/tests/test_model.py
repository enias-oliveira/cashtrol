from flask.globals import session
from app.users.tests.test_view import user_deleted
from os import name
from app.users.model import UserModel
from app.groups.model import GroupModel
from app.categories.model import CategoryModel
from app.expenses.model import ExpenseModel
from app.journal.model import JournalModel

from app.app import create_app
import app
from pytest import fixture

@fixture
def app():
    return create_app()

@fixture
def db(app):
    from app.configurations.database import db

    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        # db.session.commit()
        db.drop_all()

@fixture
def user_data():

    return{
	"name":"Fulano Rodrigues",
	"email":"fulano@email.com",
	"password_hash":"EuSouFulano123"
    }

@fixture
def group_data():

    return{
	"name":"Praia",
	"access_code":"abc123",
	"created_by":"1"
    }
@fixture
def category_data():

    return{
	"name":"Casa",
    
    }


@fixture
def journal_data():

    return{
	"name":"Casa",
    "amount": 12.89,
    "group_id": 1
	
    }
@fixture
def expenses_data():

    return{
	"description":"Casa",
    "journal_id":1,
    "category_id":1
	
    }


def test_create_journal(db, group_data, user_data, category_data, expenses_data, journal_data):

    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])
    db.session.add(user)    
    db.session.commit()

    group = GroupModel(name=group_data['name'], access_code=group_data['access_code'], created_by=group_data['created_by'])
    db.session.add(group)
    db.session.commit() 
    
    journal = JournalModel(name=journal_data['name'],amount=journal_data['amount'],group_id=journal_data['group_id']  )
    db.session.add(journal)
    db.session.commit()

    expected_name = "Casa"
    actual = JournalModel.query.get(1).name

    assert actual  == expected_name


def test_delete_journal(db, group_data, user_data, category_data, expenses_data, journal_data):

    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])
    db.session.add(user)    
    db.session.commit()

    group = GroupModel(name=group_data['name'], access_code=group_data['access_code'], created_by=group_data['created_by'])
    db.session.add(group) 
    
    journal = JournalModel(name=journal_data['name'],amount=journal_data['amount'],group_id=journal_data['group_id']  )
    db.session.add(journal)
    db.session.commit()

    table = db.session.query(JournalModel)
    deleted_expense = table.filter(JournalModel.id == 1).first()
    db.session.delete(deleted_expense)
    db.session.commit()

    actual = ExpenseModel.query.get(1)

    expected_name = None        
    actual = ExpenseModel.query.get(1)
    
    assert actual == expected_name


def test_update_journal(db, group_data, user_data, category_data, expenses_data, journal_data):

    user = UserModel(name=user_data['name'], email=user_data['email'], password_hash=user_data['password_hash'])
    db.session.add(user)    
    db.session.commit()

    group = GroupModel(name=group_data['name'], access_code=group_data['access_code'], created_by=group_data['created_by'])
    db.session.add(group) 
    
    journal = JournalModel(name=journal_data['name'],amount=journal_data['amount'],group_id=journal_data['group_id']  )
    db.session.add(journal)
    db.session.commit()

    table = db.session.query(JournalModel)
    update_journal = table.filter(JournalModel.id == 1).first()
    update_journal.name = "Show"
    db.session.add(update_journal)
    db.session.commit()

    actual = JournalModel.query.get(1)

    expected_name = "Show"        
    actual = JournalModel.query.get(1).name
    
    assert actual == expected_name