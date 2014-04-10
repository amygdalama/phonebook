import nose
import unittest

import database
import phonebook


class PhonebookTest(unittest.TestCase):
    # Whoa you can put code in a class outside a function!
    # See stackoverflow answer that Katrina sent me!
    parser = phonebook.parse()
    

    def setUp(self):
        database.create_database('test.db')
        database.create_table('test')
        database.add_record(('test_name', '888-888-8888'), 
                'test', 'test.db')


    def tearDown(self):
        database.delete_database('test.db')


class CreatePhonebook(PhonebookTest):

    def create_existing_phonebook(self):
        """Create phonebook that already exists"""

        args = parser.parse_args(['--db', 'test.db','create', 
                'test']) 

        assertRaises(Exception, phonebook.create, args)

        # assertTrue(database.table_exists('test_phonebook', args.db))



