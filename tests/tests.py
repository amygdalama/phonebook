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
TEST_NAME = 'test_name'
TEST_NUM = 'test_num'
TEST_RECORD = (TEST_NAME, TEST_NUM)

NUM_RECORDS = len(open('test_records.txt')))

# Overwrite the defaults for -b and --db
# so we can test the behavior of our script when
# we use default values for these arguments
phonebook.DEFAULT_DB = TEST_DB
phonebook.DEFAULT_PB = TEST_PB


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

            # Check that no tables were created
            nose.tools.assert_true(
                    len(database.list_tables(TEST_DB)) == 0)


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
            self.tearDown()
            self.setUp()


class NameNonexistent(unittest.TestCase):
    """Case 4: DB and table both exist but Name doesn't exist.
    Create and reverse-lookup args aren't applicable."""

    def setUp(self):
        if glob.glob('*.db'):
            raise Exception(".db files exist on setUp!")

        # Create test database and table
        database.create_database(TEST_DB)
        database.create_table(TEST_PB, TEST_DB)

        # Add some test records
        add_records()

        self.parser = phonebook.parse()

    def tearDown(self):
        for db in glob.glob('*.db'):
            database.delete_database(db)

    def test_add(self):
        """Add args should create a new record and leave other
        records alone."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'add' in args]

        for args in args_set:
            args.func(args)

            # Check that the record was added
            nose.tools.assert_true(
                    database.lookup_record(TEST_NAME, 'name', 
                            TEST_PB, TEST_DB) == [TEST_RECORD])
            
            # Check that only one record was added
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS + 1)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])

            self.tearDown()
            self.setUp()

    def test_lookup(self):
        """Lookup args should return no results."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'lookup' in args]

        for args in args_set:
            # Check that lookup returns no results
            nose.tools.assert_false(args.func(args))

            # Check that no records were added
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])

    def test_change_remove(self):
        """Change and remove args should raise Exceptions."""
        
        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'change' in args or 'remove' in args]

        for args in args_set:
            nose.tools.assert_raises(Exception, args.func, args)

            # Check that no records were added
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])


class NameExists(unittest.TestCase):
    """Case 5: DB, table, and name all exist.
    Create and reverse-lookup args aren't applicable."""

    def setUp(self):
        if glob.glob('*.db'):
            raise Exception(".db files exist on setUp!")

        # Create test database and table
        database.create_database(TEST_DB)
        database.create_table(TEST_PB, TEST_DB)

        # Add some test records
        add_records()

        # Add the test record
        database.add_record(TEST_RECORD, TEST_PB, TEST_DB)

        self.parser = phonebook.parse()

    def tearDown(self):
        for db in glob.glob('*.db'):
            database.delete_database(db)

    def test_add(self):
        """Add args should raise exceptions and not modify db."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'add' in args]

        for args in args_set:
            nose.tools.assert_raises(Exception, args.func, args)

            # Check that the test record hasn't been modified
            nose.tools.assert_true(database.lookup_record(
                    TEST_NAME, 'name', TEST_PB, TEST_DB) == [TEST_RECORD])

            # Check that no other records were added
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS + 1)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])

    def test_change(self):
        """Change args should change the record."""

        new_num = 'test_new_num'
        new_record = (TEST_NAME, new_num)

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'change' in args]

        for args in args_set:
            args.func(args)

            # Check that the test record has been modified
            nose.tools.assert_true(database.lookup_record(
                    TEST_NAME, 'name', TEST_PB, TEST_DB) == [new_record])

            # Check that no other records were added
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS + 1)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])

            self.tearDown()
            self.setUp()

    def test_lookup(self):
        """Lookup args should return the record."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'lookup' in args]

        for args in args_set:
            # Check that lookup returns the correct record
            nose.tools.assert_true(args.func(args) == [TEST_RECORD])

            # Check that the test record hasn't been modified
            nose.tools.assert_true(database.lookup_record(
                    TEST_NAME, 'name', TEST_PB, TEST_DB) == [TEST_RECORD])

            # Check that no records were added
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS + 1)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])

    def test_remove(self):
        """Remove args should remove the record."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'remove' in args]

        for args in args_set:
            args.func(args)

            # Check that the record has been deleted
            nose.tools.assert_false(database.lookup_record(
                TEST_NAME, 'name', TEST_PB, TEST_DB))

            # Check that there's one less record
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])

            self.tearDown()
            self.setUp()

        def test_all_else(self):
            """Change and reverse-lookup should raise Exceptions. 
            Script isn't ready for this though."""
            pass


class NumberNonexistent(unittest.TestCase):
    """Case 6: DB and table both exist but Number doesn't exist.
    Add, Change, Remove, Lookup args aren't applicable."""

    def setUp(self):
        if glob.glob('*.db'):
            raise Exception(".db files exist on setUp!")

        # Create test database and table
        database.create_database(TEST_DB)
        database.create_table(TEST_PB, TEST_DB)

        # Add some test records
        add_records()

        self.parser = phonebook.parse()

    def tearDown(self):
        for db in glob.glob('*.db'):
            database.delete_database(db)

    def test_reverse_lookup(self):
        """Reverse-lookup args should return no results."""
        
        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'reverse-lookup' in args]

        for args in args_set:
            # Check that lookup returns no results
            nose.tools.assert_false(args.func(args))

            # Check that no records were added
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])

    def test_all_else(self):
        """All other args should raise exceptions. Script isn't ready
        for this yet, though."""
        pass


class NumberExists(unittest.TestCase):
    """Case 7: DB, table, and Number all exist."""

    def setUp(self):
        if glob.glob('*.db'):
            raise Exception(".db files exist on setUp!")

        # Create test database and table
        database.create_database(TEST_DB)
        database.create_table(TEST_PB, TEST_DB)

        # Add some test records
        add_records()

        # Add the test record
        database.add_record(TEST_RECORD, TEST_PB, TEST_DB)

        self.parser = phonebook.parse()

    def tearDown(self):
        for db in glob.glob('*.db'):
            database.delete_database(db)

    def test_reverse_lookup(self):
        """Reverse-lookup should return result."""

        args_set = [self.parser.parse_args(args) for args in read_args()
                if 'reverse-lookup' in args]

        for args in args_set:
            # Check that lookup returns the correct record
            nose.tools.assert_true(args.func(args) == [TEST_RECORD])

            # Check that the test record hasn't been modified
            nose.tools.assert_true(database.lookup_record(
                    TEST_NUM, 'number', TEST_PB, TEST_DB) == [TEST_RECORD])

            # Check that no records were added
            nose.tools.assert_true(
                    len(database.read_table(
                            TEST_PB, TEST_DB)) == NUM_RECORDS + 1)

            # Check that all other records remain the same
            for record in read_records():
                nose.tools.assert_true(database.lookup_record(
                        record[0], 'name', TEST_PB, TEST_DB) == [record])

    def test_all_else(self):
        """Other args should raise Exceptions, but script isn't ready
        for this yet."""
        pass


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



