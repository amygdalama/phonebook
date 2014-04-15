import os
import sqlite3

# TODOs:
# Find a way to write queries without using string interpolation


def create_database(filename):
    if database_exists(filename):
        raise Exception("That database already exists!")
    
    else:
        with sqlite3.connect(filename) as con:
            pass


def delete_database(filename):
    os.remove(filename)   


def database_exists(filename):
    """Checks to see if a given database exists.
    Right now only checks to see if the file exists,
    but eventually I should change this to check that
    the file is a sqlite3 database."""

    return os.path.exists(filename)    


def table_exists(table, database):
    """Checks to see if a table exists in a database."""

    return table in list_tables(database)


def list_tables(database):
    """Retrieves the list of table names in a database"""
    
    with sqlite3.connect(database) as con:
        c = con.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in c.fetchall()]


def create_table(table, database):
    if not database_exists(database):
        raise Exception("That database doesn't exist!")
    else:
        with sqlite3.connect(database) as con:
            c = con.cursor()
            c.execute("CREATE TABLE %s (name text, number text)" % table)


def read_table(table, database):
    if not database_exists(database):
        raise Exception("That database doesn't exist!")

    else:
        with sqlite3.connect(database) as con:
            c = con.cursor()
            c.execute("SELECT * FROM %s" % table)

        return c.fetchall()

def lookup_record(value, column, table, database):
    """Checks to see if a specific value exists in the given column
    in the given database table."""

    if not database_exists(database):
        raise Exception("That database doesn't exist!")
    else:
        # sqlite3 throws exceptions when table or column
        # doesn't exist
        with sqlite3.connect(database) as con:
            c = con.cursor()
            c.execute("SELECT * FROM %s WHERE %s=?" % 
                    (table, column), (value,))

        return c.fetchall()


def add_record(values, table, database):
    if not database_exists(database):
        raise Exception("That database doesn't exist!")
    elif lookup_record(values[0], 'name', table, database):
        raise Exception("%s already exists in %s!" %
                (values[0], table))
    else:    
        with sqlite3.connect(database) as con:
            c = con.cursor()
            c.execute("INSERT INTO %s VALUES %s" % (table, values))  


def delete_record(value, column, table, database):
    if not database_exists(database):
        raise Exception("That database doesn't exist!")
    elif not lookup_record(value, column, table, database):
        raise Exception("That record doesn't exist in the database!")
    else:
        with sqlite3.connect(database) as con:
            c = con.cursor()
            c.execute("DELETE FROM %s WHERE %s=?" % 
                    (table, column), (value,))

def tables_equal(table1, database1, table2, database2):

    if not database_exists(database1):
        raise Exception("%s doesn't exist!" % database1)

    elif not database_exists(database2):
        raise Exception("%s doesn't exist!" % database2)

    elif not table_exists(table1, database1):
        raise Exception("%s doesn't exist in %s!" % (table1, database1))

    elif not table_exists(table2, database2):
        raise Exception("%s doesn't exist in %s!" % (table2, database2))

    return read_table(table1, database1) == read_table(table2, database2)


def databases_equal(database1, database2):
    """Checks to see if two databases are identical."""

    # TODO: allow any number of databases as parameters

    if not database_exists(database1):
        raise Exception("%s doesn't exist!" % database1)

    elif not database_exists(database2):
        raise Exception("%s doesn't exist!" % database2)

    tables1 = list_tables(database1)
    tables2 = list_tables(database2)

    if tables1 != tables2:
        print "tables unequal"
        print "database1 :", database1
        print "tables1: ", tables1
        print "database2: ", database2
        print "tables2: ", tables2
        return False

    else:
        for table in tables1:
            if read_table(table, database1) != read_table(table, database2):
                return False

        return True


if __name__ == '__main__':
    values = ('Charles', '888-8888')
    add_record(values, 'phonebook', 'phonebook.db')
    print lookup_record('Charles', 'name', 'phonebook', 'phonebook.db')
    delete_record('Charles', 'name', 'phonebook', 'phonebook.db')
    print lookup_record('Charles', 'name', 'phonebook', 'phonebook.db')

