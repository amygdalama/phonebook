## Tests

### Add

* case 1:
    * database - doesn't exist
    * raise exception
* case 2:
    * database - exists
    * table - doesn't exist
    * raise exception
* case 3:
    * database - exists
    * table - exists 
    * record - exists
    * raise exception
* case 4:
    * database - exists
    * table - exists
    * record - doesn't exist
    * add record

### Change

* case 1:
    * database - doesn't exist
    * raise exception
* case 2:
    * database - exists
    * table - doesn't exist
    * raise exception
* case 3:
    * database - exists
    * table - exists
    * record - doesn't exist
    * raise exception
* case 4:
    * database - exists
    * table - exists 
    * record - exists
    * change record

### Create

* case 1:
    * database - doesn't exist
    * raise exception
* case 2:
    * database - exists
    * table - exists
    * raise exception
* case 3:
    * database - exists
    * table - doesn't exist
    * create table
* table and database both exist => throw error
* database exists but table doesn't => add table
* database doesn't exist => throw error

### Lookup

### Remove

### Reverse-Lookup