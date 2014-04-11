import sys
import unittest

import nose

# add parent directory to import database and phonebook scripts
# how can I make the database and phonebook modules available
# in a more elegant way? Would making this group of scripts a
# "package" solve this problem?
sys.path.insert(0, '../')

import database
import phonebook


TEST_DB = 'test.db'
TEST_PB = 'test'

UNEDITED_DB = 'unedited.db'
UNEDITED_PB = 'test'

NONEXISTENT_DB = 'nonexistent.db'
NONEXISTENT_PB = 'nonexistent'


class PhonebookTest(unittest.TestCase):

    def setUp(self):

        database.create_database(TEST_DB)
        database.create_database(UNEDITED_DB)

        if database.database_exists(NONEXISTENT_DB):
            database.delete_database(NONEXISTENT_DB)

        # This is in a try/except because if it doesn't
        # work I want to delete the database
        try:
            database.create_table(TEST_PB, TEST_DB)
            database.add_record(('test_name', '888-888-8888'), 
                    TEST_PB, TEST_DB)
            database.create_table(UNEDITED_PB, UNEDITED_DB)
            database.add_record(('test_name', '888-888-8888'), 
                    UNEDITED_PB, UNEDITED_DB)
        except:
            database.delete_database(TEST_DB)
            database.delete_database(UNEDITED_DB)
            raise Exception("Couldn't add test records")


    def tearDown(self):
        database.delete_database(TEST_DB)
        database.delete_database(UNEDITED_DB)
        if database.database_exists(NONEXISTENT_DB):
            raise Exception("nonexistent.db wasn't deleted")


class CreatePhonebook(PhonebookTest):
        

    def test_db_doesnt_exist(self):
        """Create phonebook in a database that doesn't exist.

        First we ensure that creating a phonebook in a nonexistent
        database raises an Exception. Then we ensure that the nonexistent
        database wasn't created."""

        # Override defaults from config file to test defaults.
        # Is there a better way to do this?
        # Also - it's really interesting that this actually works!
        phonebook.DEFAULT_DB = NONEXISTENT_DB
        phonebook.DEFAULT_PB = NONEXISTENT_PB

        parser = phonebook.parse()

        args_set = (['create', phonebook.DEFAULT_PB],
                ['-b', phonebook.DEFAULT_PB, 'create', phonebook.DEFAULT_PB],
                ['--db', phonebook.DEFAULT_DB, 'create', phonebook.DEFAULT_PB],
                ['-b', phonebook.DEFAULT_PB, '--db', phonebook.DEFAULT_DB, 'create', phonebook.DEFAULT_PB])

        for args in args_set:
            args = parser.parse_args(args)
            nose.tools.assert_raises(Exception, phonebook.create, args)
            nose.tools.assert_false(database.database_exists(NONEXISTENT_DB))
    

    def test_both_pb_and_db_exist(self):
        """Create phonebook that already exists in a database
        that already exists.

        Since TEST_DB and TEST_PB are created on setUp, we should
        expect an Exception to be thrown when we try creating the
        TEST_PB inside the TEST_DB again. After our attempt, we 
        check to see if the original TEST_DB is unchanged."""

        phonebook.DEFAULT_DB = TEST_DB
        phonebook.DEFAULT_PB = TEST_PB

        parser = phonebook.parse()

        args_set = (['create', phonebook.DEFAULT_PB],
                ['-b', phonebook.DEFAULT_PB, 'create', phonebook.DEFAULT_PB],
                ['--db', phonebook.DEFAULT_DB, 'create', phonebook.DEFAULT_PB],
                ['-b', phonebook.DEFAULT_PB, '--db', phonebook.DEFAULT_DB, 'create', phonebook.DEFAULT_PB])

        for args in args_set:
            args = parser.parse_args(args) 
            nose.tools.assert_raises(Exception, phonebook.create, args)
            nose.tools.assert_true(database.databases_equal(
                    TEST_DB, UNEDITED_DB))


    def test_db_exists_but_not_pb(self):
        """Create phonebook that doesn't already exist in a
        database that already exists.

        First check to make sure the table was created, and then 
        make sure the other existing table was unchanged.

        Delete the database after we run the test."""
        
        phonebook.DEFAULT_DB = TEST_DB
        phonebook.DEFAULT_PB = NONEXISTENT_PB

        parser = phonebook.parse()

        args_set = (['create', phonebook.DEFAULT_PB],
                ['-b', phonebook.DEFAULT_PB, 'create', phonebook.DEFAULT_PB],
                ['--db', phonebook.DEFAULT_DB, 'create', phonebook.DEFAULT_PB],
                ['-b', phonebook.DEFAULT_PB, '--db', phonebook.DEFAULT_DB, 'create', phonebook.DEFAULT_PB])

        for args in args_set:
            args = parser.parse_args(args)
            nose.tools.assert_true(database.table_exists(
                    NONEXISTENT_PB, TEST_DB))

            database.delete_database(NONEXISTENT_DB)



