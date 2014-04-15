import glob
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
TEST_PB = 'test_phonebook'


class DatabaseNonexistent(unittest.TestCase):
    """Test case 1: database doesn't exist.
    Every argument should raise an Exception for this case."""

    def setUp(self):
        if glob.glob('*.db'):
            raise Exception(".db files exist on setUp!")

    def tearDown(self):
        if glob.glob('*.db'):
            for db in glob.glob('*.db'):
                database.delete_database(db)
            raise Exception("New .db files were unintentionally created!")

    def test_all(self):

        # Overwrite the defaults for -b and --db
        # so we can test the behavior of our script when
        # we use default values for these arguments
        phonebook.DEFAULT_DB = TEST_DB
        phonebook.DEFAULT_PB = TEST_PB
        parser = phonebook.parse()
        args_set = [parser.parse_args(args) for args in read_args()]
        
        for args in args_set:
            nose.tools.assert_raises(Exception, args.func, args)


class TableNonExistent(unittest.TestCase):
    """Test case 2: table doesn't exist in database.
    Every argument except `create` should raise an Exception."""

    def setUp(self):
        if glob.glob('*.db'):
            raise Exception(".db files exist on setUp and shouldn't!")
        database.create_database(TEST_DB)

        phonebook.DEFAULT_DB = TEST_DB
        phonebook.DEFAULT_PB = TEST_PB
        self.parser = phonebook.parse()

    def tearDown(self):
        for db in glob.glob('*.db'):
            database.delete_database(db)

    def test_create(self):
        """Tests the create argument, which should create a new table."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'create' in args]
        for args in args_set:
            args.func(args)

            # Check that the table was created
            nose.tools.assert_true(
                    database.table_exists(TEST_PB, TEST_DB))

            # Check that only one table was created
            nose.tools.assert_true(
                    len(database.list_tables(TEST_DB)) == 1)

            # Check that no records were added
            nose.tools.assert_true(
                    len(database.read_table(TEST_PB, TEST_DB)) == 0)

            # Delete and recreate TEST_DB
            # There's probably a better way to do this
            self.tearDown()
            self.setUp()

    def test_all_else(self):
        """Tests all arguments besides the create argument.
        These should all raise Exceptions."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'create' not in args]
        for args in args_set:
            nose.tools.assert_raises(Exception, args.func, args)


class BothDatabaseAndTableExist(unittest.TestCase):
    """Case 3: Both Database and Table Exist. Attempting to
    create the table should raise an Exception and leave the existing
    table in tact."""

    def setUp(self):
        if glob.glob('*.db'):
            raise Exception(".db files exist on setUp!")

        # Create test database and table
        database.create_database(TEST_DB)
        database.create_table(TEST_PB, TEST_DB)

        # Add some test records
        add_records()

        phonebook.DEFAULT_DB = TEST_DB
        phonebook.DEFAULT_PB = TEST_PB
        self.parser = phonebook.parse()

    def tearDown(self):
        for db in glob.glob('*.db'):
            database.delete_database(db)

    def test_create(self):
        """Test the create arguments, which should raise Exceptions."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'create' in args]

        for args in args_set:
            nose.tools.assert_raises(Exception, args.func, args)
            print database.read_table(TEST_PB, TEST_DB)
            self.tearDown()
            self.setUp()


def read_args():
    """Reads arguments from the arguments.txt file and returns
    a nested list of all possible arguments."""

    return [line.split() for line in open('arguments.txt')]

def read_records():
    """Reads test records from test_records.txt."""
    return [tuple(line.strip().split('\t')) for line in open('test_records.txt')]

def add_records(pb=TEST_PB, db=TEST_DB):
    """Adds test records to the test database."""

    records = read_records()
    for record in records: database.add_record(record, pb, db)



