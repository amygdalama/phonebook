import os
import unittest
import nose
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import phonebook
from alchemy import Base, Contact

TEST_RECORDS = {'Sarah' : '123-123-1234',
                'Martin' : '234-234-2345',
                'Jessica' : '345-345-3456',
                'Alex' : '456-456-4567'}

if os.path.exists('test.db'):
    os.remove('test.db')
engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
for name, number in TEST_RECORDS.items():
    test_contact = Contact(name=name, number=number)
    session.add(test_contact)
session.commit()

class AddRecord(unittest.TestCase):
    def setUp(self):
        phonebook.add(name='test_name', number='test_number', 
                session=session)
    
    def tearDown(self):
        results = session.query(Contact).filter_by(name='test_name')
        for result in results:
            session.delete(result)
            session.commit()

    def test_added(self):
        assert len(session.query(Contact).filter_by(name=name).all()) == 1
    
    def test_all_else_equal(self):
        assert len(session.query(Contact).all()) == 5

class RemoveRecord(unittest.TestCase):
    def setUp(self):
        phonebook.remove(name='Sarah', session=session)

    def tearDown(self):
        contact = Contact(name='Sarah', number='123-123-1234')
        session.add(contact)
        session.commit()

    def test_removed(self):
        assert len(session.query(Contact).filter_by(name='Sarah').all()) == 0

    def test_all_else_equal(self):
        assert len(session.query(Contact).all()) == 3