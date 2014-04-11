#! /usr/bin/env python

import argparse

import config
import database


DEFAULT_DB = config.DEFAULT_DB or 'phonebook.db'
DEFAULT_PB = config.DEFAULT_PB or 'phonebook'


def print_lookup_results(records, value, phonebook):

    if records:
        for record in records:
            print "%s\t%s" % (record[0], record[1])
    else:
        print "%s isn't in %s." % (value, phonebook)



def add(args):
    """Invoked with the `add` command line argument. Attempts to add 
    an entry to a specified phonebook. Raises exceptions if the phonebook
    doesn't exist or if the entry already exists in the phonebook."""

    print "add function called"
    if not database.table_exists(args.b, args.db):
        raise Exception("%s doesn't exist" % args.b)

    # To-do: change this to also print out the existing phone number
    if database.lookup_record(args.name, 'name', args.b, args.db):
        raise Exception("%s already exists in %s. "
            "Use the `change` command to update the existing entry."
            % (args.name, args.b))

    else:
        database.add_record((args.name, args.number), args.b, args.db)
        print "Added the following entry to %s:" % args.b
        print "%s\t%s" % (args.name, args.number)


def change(args):
    
    remove(args)
    add(args)


def create(args):
    """Invoked with the `create` command line argument.
    Creates a new table (phonebook) in the given database. Throws an exception
    if the table already exists in the database."""

    if database.table_exists(args.b, args.db):
        raise Exception("Phonebook %s already exists in the database %s." % (
                    args.b, args.db))

    else:
        database.create_table(args.b, args.db)

    print "Created phonebook %s in the %s database." % (args.b, args.db)


def lookup(args):

    # TODOs:
    # Allow for looking up against all phonebooks
    # Allow for partial matching
    if not database.table_exists(args.b, args.db):
        raise Exception("%s doesn't exist in %s" % (args.b, args.db))

    records = database.lookup_record(args.name, 'name', args.b, args.db)
    
    print_lookup_results(records, args.name, args.b)

    return records


def remove(args):

    if not database.table_exists(args.b, args.db):
        raise Exception("%s doesn't exist in %s" % (args.b, args.db))

    if not database.lookup_record(args.name, 'name', args.b, args.db):
        raise Exception("%s doesn't exist in %s." % (args.name, args.b))
    
    database.delete_record(args.name, 'name', args.b, args.db)
    print "Removed %s from %s." % (args.name, args.b)


def reverse_lookup(args):

    # TODOs:
    # Allow for looking up against all phonebooks
    # Allow for partial matching
    if not database.table_exists(args.b, args.db):
        raise Exception("%s doesn't exist in %s" % (args.b, args.db))

    records = database.lookup_record(args.number, 'number', args.b, args.db)

    print_lookup_results(records, args.number, args.b)
    
    return records


def parse():
    parser = argparse.ArgumentParser(description='A phonebook command line tool!')

    # To-do: -b right now only works if it's put before the subparser commands
    # How can I elegantly make this option available to all subparsers
    # (after the subparser commands) without adding it manually to each
    # subparser?
    parser.add_argument('-b', default=DEFAULT_PB,
            help="name of the phonebook table in the database") 
    parser.add_argument('--db', default=DEFAULT_DB, 
            help="name of the database file")   

    # Adding subparsers so that different commands can have different
    # required positional arguments
    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('name', help="name of person as a string")
    parser_add.add_argument('number', help="phone number as a string")
    parser_add.set_defaults(func=add)

    # Could be same parser as 'add' - takes same arguments
    parser_change = subparsers.add_parser('change')
    parser_change.add_argument('name', help="name of person as a string")
    parser_change.add_argument('number', help="phone number as a string")   
    parser_change.set_defaults(func=change) 

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('b', help="name of phonebook table in database")
    parser_create.set_defaults(func=create)

    parser_lookup = subparsers.add_parser('lookup')
    parser_lookup.add_argument('name')
    parser_lookup.set_defaults(func=lookup)

    parser_remove = subparsers.add_parser('remove')
    parser_remove.add_argument('name', help="name of person as a string")
    parser_remove.set_defaults(func=remove)

    parser_reverse_lookup = subparsers.add_parser('reverse-lookup')
    parser_reverse_lookup.add_argument('number', help="phone number as a string")
    parser_reverse_lookup.set_defaults(func=reverse_lookup)

    return parser   


if __name__ == '__main__':
    parser = parse()
    args = parser.parse_args() 

    if args.db != DEFAULT_DB and not database.database_exists(args.db):
        raise Exception("Database %s doesn't exist!" % args.db)
    
    args.func(args)

# General things:
# Should I pass var(args) to these functions and use kwargs instead?
# There's a lot of repetition/duplication in my exception handling.