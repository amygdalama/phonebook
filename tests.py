import nose
import unittest

import database
import phonebook


class PhonebookTest(unittest.TestCase):
    # Whoa you can put code in a class outside a function!
    # See stackoverflow answer that Katrina sent me!

    def setUp(self):
        self.parser = phonebook.parse()
        database.create_database('test.db')

        try:
            database.create_table('test', 'test.db')
            database.add_record(('test_name', '888-888-8888'), 
                    'test', 'test.db')
        except:
            database.delete_database('test.db')
            raise Exception("Couldn't add test records")


    def tearDown(self):
        database.delete_database('test.db')


class CreatePhonebook(PhonebookTest):

    def test_create_existing_phonebook(self):
        """Create phonebook that already exists"""

        args = self.parser.parse_args(['--db', 'test.db','create', 
                'test']) 

        # This is cool this actually executes the code in
        # phonebook.create so later we can test for side-effects
        nose.tools.assert_raises(Exception, phonebook.create, args)
        print "Hello"
        print database.lookup_record('bad_thing', 'name', args.b, args.db)

        # assertTrue(database.table_exists('test_phonebook', args.db))



