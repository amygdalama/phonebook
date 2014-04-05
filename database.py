import sqlite3

# TODOs:
# Find a way to write queries without using string interpolation


def database_exists(filename):
    """Checks to see if a given database exists"""

    return os.path.exists(filename)    


def list_tables(database):
    """Retrieves the list of table names in a database"""
    
    with sqlite3.connect(database) as con:
        c = con.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in c.fetchall()]


def table_exists(table, database):
    """Checks to see if a table exists in a database"""
    
    return table in list_tables(database)


def create_table(table, database):
    with sqlite3.connect(database) as con:
        c = con.cursor()
        c.execute("CREATE TABLE %s (name text, number text)" % table)


def read_table(table, database):
    with sqlite3.connect(database) as con:
        c = con.cursor()    


def lookup_record(value, column, table, database):
    """Checks to see if a specific value exists in the given column
    in the given database table."""

    with sqlite3.connect(database) as con:
        c = con.cursor()
        c.execute("SELECT * FROM %s WHERE %s=?" % (table, column), (value,))

    return c.fetchall()


def add_record(values, table, database):
    with sqlite3.connect(database) as con:
        c = con.cursor()
        c.execute("INSERT INTO %s VALUES %s" % (table, values))  


if __name__ == '__main__':
    # values = ('Sarah', '888-8888')
    # add_record(values, 'phonebook', 'phonebook.db')
    print lookup_record('Sarah', 'name', 'phonebook', 'phonebook.db')

