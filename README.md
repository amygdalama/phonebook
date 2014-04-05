A phonebook command line tool!

Usage:
    
    $ phonebook create 'PhonebookName'  # no spaces
    $ phonebook add 'Name' 'Number'
    $ phonebook remove 'Name'
    $ phonebook change 'Name' 'New Number'
    $ phonebook lookup 'Name'
    $ phonebook reverse-lookup 'Number'

Most commands also have the `-b` and `--db` options:

    $ phonebook -b 'phonebook_name' --db 'database_name' 'Name' 'Number'


TODOs:

* Figure out how to get this to work on someone else's computer without them having to add a symlink on their `$PATH`
* Standardize phone number entries
* Better use of `argparse`
* Allow search by partial name
* Allow `-b phonebook` to occur anywhere in command
* Case insensitive search
* Make names work without using quotes
* Add a config file where you can specify a default phone book to use. Add commands to edit this file without having to edit it manually
* Implement a http backend (`phonebook lookup Tom -b 'http://mywebsite/phonebook'` etc.)
* Add tab completion