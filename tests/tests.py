import sys
import unittest

import nose

# add parent directory to import database and phonebook scripts
sys.path.insert(0, '../')

import database
import phonebook


class PhonebookTest(unittest.TestCase):

    def setUp(self):

        # Override defaults from config file to test defaults.
        # Is there a better way to do this?
        # Also - it's really interesting that this actually works!
        phonebook.DEFAULT_DATABASE = 'test.db'
        phonebook.DEFAULT_PHONEBOOK = 'test'
        
        self.parser = phonebook.parse()
        database.create_database('test.db')
        database.create_database('unedited.db')

        # This is in a try/except because if it doesn't
        # work I want to delete the database
        try:
            database.create_table('test', 'test.db')
            database.add_record(('test_name', '888-888-8888'), 
                    'test', 'test.db')
            database.create_table('test', 'unedited.db')
            database.add_record(('test_name', '888-888-8888'), 
                    'test', 'unedited.db')
        except:
            database.delete_database('test.db')
            database.delete_database('unedited.db')
            raise Exception("Couldn't add test records")


    def tearDown(self):
        database.delete_database('test.db')
        database.delete_database('unedited.db')


class CreatePhonebook(PhonebookTest):

    def test_create_existing_phonebook(self):
        """Create phonebook that already exists"""

        args_set = (['create', 'test'],
                    ['-b', 'test', 'create', 'test'],
                    ['--db', 'test.db', 'create', 'test'],
                    ['-b', 'test', '--db', 'test.db', 'create', 'test'])

        for args in args_set:

            args = self.parser.parse_args(args) 
            nose.tools.assert_raises(Exception, phonebook.create, args)
            nose.tools.assert_true(database.databases_equal(
                    'test.db', 'unedited.db'))

    def test_create_new_phonebook(self):
        """Create phonebook that doesn't already exist."""

        args_set = (['create', 'test'],
                    ['-b', 'test', 'create', 'test'],
                    ['--db', 'test.db', 'create', 'test'],
                    ['-b', 'test', '--db', 'test.db', 'create', 'test'])        



