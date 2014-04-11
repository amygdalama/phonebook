# Tests

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
        * add raises exception
        * change raises exception
        * create creates new table
            * assert new table exists
            * assert previous table unchanged
        * lookup raises exception
        * remove raises exception
        * reverse-lookup raises exception

## case 3:
    * properties
        * database and table both exist
    * assert
        * create raises exception

## case 4:
    * properties
        * database and table both exist
        * name doesn't exist
    * assert
        * add creates new record for name
            * assert correct record was added
            * assert no other records were added
            * assert no other tables were added
            * assert no other databases were created
        * lookup raises Exception
        










==============================
Commands
==============================

* Add

* Change

* Create

* Lookup

* Remove

* Reverse-Lookup



