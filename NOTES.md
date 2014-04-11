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
    * properties
        * database - doesn't exist
    * assert
        * raises exception
* case 2:
    * database - exists
    * table - exists
    * raise exception
* case 3:
    * database - exists
    * table - doesn't exist
    * create table

### Lookup

### Remove

### Reverse-Lookup



## case 1:
    * properties
        * database doesn't exist
        * parser arguments
            * db = NONEXISTENT
            * nothing else matters
    * assert
        * add raises exception
        * change raises exception
        * create raises expection
        * lookup raises exception
        * remove raises exception
        * reverse-lookup raises exception
## case 2:
    * properties
        * database exists but table doesn't exist
        * parser args
            * db = TEST
            * table = NONEXISTENT
    * assert
        * add
        * change
        * create
        * lookup
        * remove
        * reverse-lookup