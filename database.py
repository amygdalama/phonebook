import sqlite3


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

