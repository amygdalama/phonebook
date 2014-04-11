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
TEST_NUM = 'test_number'


class DatabaseNonexistent(unittest.TestCase):
    """Tests the commands in the case that the given database
    doesn't exist."""

    def setUp(self):
        if glob.glob('*.db'):
            raise Exception(".db files exist on setUp!")

    def tearDown(self):
        for db in glob.glob('*.db'):
            database.delete_database(db)

    def add(self):

        # Overwrite the defaults for -b and --db
        # so we can test the behavior of our script when
        # we use default values for these arguments
        phonebook.DEFAULT_DB = TEST_DB
        phonebook.DEFAULT_PB = TEST_PB
        parser = phonebook.parse()

        args_set = [parser.parse_args(args) for args in read_args('add')]
        for args in args_set:
            nose.assert_raises(Exception, phonebook.add, args)



def read_args(arg):
    args_set = [line.split() for line in open('arguments.txt') 
            if arg in line.split()]
    
    return args_set