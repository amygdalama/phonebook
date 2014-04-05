#! /usr/bin/env python

import argparse
import glob
import os
import pprint
import sqlite3

import database


DEFAULT_DATABASE = 'phonebook.db'
DEFAULT_PHONEBOOK = 'phonebook'


def load_phonebooks():
    """Finds all the .pb files in the current directory, reads them,
    and returns a list of the phonebook dictionaries"""
    
    filenames = glob.glob("*.pb")

    return [read_phonebook(filename) for filename in filenames]


def read_phonebook(filename):
    """Reads the given filename and returns a dictionary containing the
    phonebook entries"""

    phonebook = {}

    with open(filename, 'r') as phonebook_file:

        for line in phonebook_file:
            line = line.rstrip('\n').split('\t')
            phonebook[line[0]] = line[1]

    return phonebook


def write_phonebook(phonebook, filename):
    """Writes a phonebook -- given by a dictionary -- to a file."""
    with open(filename, 'w') as phonebook_file:
        for key, value in phonebook.items():
            phonebook_file.write(key + '\t' + value + '\n')


def entry_exists(name, filename):
    """Checks to see if the given name already exists in the given phonebook."""

    # Reads the phonebook file and returns a dictionary with the entries
    phonebook = read_phonebook(filename)
    
    return name in phonebook


def add_entry(name, number, filename):
    """Adds an entry to a given phonebook, assuming that the entry doesn't
    already exist in the phonebook."""

    with open(filename, 'a') as phonebook_file:
        phonebook_file.write(args.name + '\t' + args.number + '\n')


def remove_entry(name, filename):
    """Removes an entry from a given phonebook"""

    phonebook = read_phonebook(filename)

    if name in phonebook:
        del phonebook[name]
        write_phonebook(phonebook, filename)

    else:
        raise Exception("Hold up %s doesn't exist in %s." % (name, filename))


def add(args):
    """Invoked with the `add` command line argument. Attempts to add 
    an entry to a specified phonebook. Raises exceptions if the phonebook
    doesn't exist or if the entry already exists in the phonebook."""

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

    if not args.b:
        raise Exception("Yo, you need to provide a phonebook with -b")

    if not database.table_exists(args.b):
        raise Exception("%s doesn't exist" % args.b)

    if not entry_exists(args.name, args.b):
        raise Exception("%s doesn't exist in %s." % (args.name, args.b))
    
    remove_entry(args.name, args.b)
    add_entry(args.name, args.number, args.b)        


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
    if args.b:
        
        if not database.table_exists(args.b):
            raise Exception("%s doesn't exist" % args.b)

        phonebook = read_phonebook(args.b)
        
        if args.name in phonebook:
            print "Name: %s, Number: %s" % (args.name, phonebook[args.name])
            return phonebook[args.name]
        else:
            print "%s isn't in %s." % (args.name, args.b)
            return

    else:

        # A list of phonebooks, which are dictionaries
        # It seems super wasteful to have all this in memory!
        phonebooks = load_phonebooks()
        results = []
        for phonebook in phonebooks:
            if args.name in phonebook:
                results.append((args.name, phonebook[args.name]))

        if results:
            for entry in results:
                print "%s\t%s" % (entry[0], entry[1])
        else:
            print "Oh noes! %s wasn't found in any phonebook!" % args.name

        return results


def remove(args):
    if not args.b:
        raise Exception("Yo, you need to provide a phonebook with -b")

    if not database.table_exists(args.b):
        raise Exception("%s doesn't exist" % args.b)

    if not entry_exists(args.name, args.b):
        raise Exception("%s doesn't exist in %s." % (args.name, args.b))
    
    remove_entry(args.name, args.b)


def reverse_lookup(args):
    if args.b:
        
        if not database.table_exists(args.b):
            raise Exception("%s doesn't exist" % args.b)

        phonebook = read_phonebook(args.b)

        # Flip keys and values to lookup by number
        phonebook = dict(zip(phonebook.values(), phonebook.keys()))
        
        if args.number in phonebook:
            print "Name: %s, Number: %s" % (phonebook[args.number], args.number)
            return phonebook[args.number]
        else:
            print "%s isn't in %s." % (args.number, args.b)
            return

    else:

        # A list of phonebooks, which are dictionaries
        # It seems super wasteful to have all this in memory!
        phonebooks = load_phonebooks()
        results = []
        for phonebook in phonebooks:
            phonebook = dict(zip(phonebook.values(), phonebook.keys()))
            if args.number in phonebook:
                results.append((phonebook[args.number], args.number))

        if results:
            for entry in results:
                print "%s\t%s" % (entry[0], entry[1])
        else:
            print "Oh noes! %s wasn't found in any phonebook!" % args.number

        return results


def parse():
    parser = argparse.ArgumentParser(description='A phonebook command line tool!')

    # To-do: -b right now only works if it's put before the subparser commands
    # How can I elegantly make this option available to all subparsers
    # (after the subparser commands) without adding it manually to each
    # subparser?
    parser.add_argument('-b', default=DEFAULT_PHONEBOOK,
            help="name of the phonebook table in the database") 
    parser.add_argument('--db', default=DEFAULT_DATABASE, 
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

    args = parser.parse_args() 

    return args   


if __name__ == '__main__':
    args = parse()

    if args.db != DEFAULT_DATABASE and not database.database_exists(args.db):
        raise Exception("Database %s doesn't exist!" % args.db)
    
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    args.func(args)

    # General things:
    # Should I pass var(args) to these functions and use kwargs instead?
    # There's a lot of repetition/duplication in my exception handling.
    # I should try using a database!
    # I attemped to make this code easy-ish to transfer to a database...
    # How could I have done that better?
