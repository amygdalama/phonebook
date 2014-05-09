#! /usr/bin/env python

import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from alchemy import Base, Contact
import database


def print_lookup_results(records):
    if records:
        for record in records:
            print "%s\t%s" % (record.name, record.number)
    else:
        print "No phonebook entries found."

def add(name, number):
    """Invoked with the `add` command line argument. Attempts to add 
    an entry to a specified phonebook. Raises exceptions if the phonebook
    doesn't exist or if the entry already exists in the phonebook."""
    new_contact = Contact(name=name, number=number)
    session.add(new_contact)
    session.commit()
    print "Added the new contact:"
    print "%s\t%s" % (name, number)

def change(name, number):
    records = lookup(name)
    if records:
        print "Updated the following entries:"
        for record in records:
            record.number = number
            print "%s\t%s" % (record.name, record.number)
        session.commit()
    else:
        print "No phonebook entries found."

def lookup(name):
    records = session.query(Contact).filter_by(name=name).all()
    return records

def remove(name): 
    records = lookup(name)
    if records:
        print "Deleted the following entries:"
        for record in records:
            session.delete(record)
            print "%s\t%s" % (record.name, record.number)
        session.commit()
    else:
        print "No phonebook entries found."

def reverse_lookup(number):
    records = session.query(Contact).filter_by(number=number).all()
    return records

def parse_args():
    parser = argparse.ArgumentParser(description='A phonebook command line tool!')

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
    engine = create_engine('sqlite:///sqlalchemy_phonebook.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    parser = parse_args()
    args = parser.parse_args() 
    func = args.func
    del args.func
    results = func(**vars(args))
    if results != None:     # execute even if results == []
        print_lookup_results(results)