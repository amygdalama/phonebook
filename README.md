A phonebook command line tool!

##Usage
    
    $ phonebook add 'Name' 'Number'
    $ phonebook remove 'Name'
    $ phonebook change 'Name' 'New Number'
    $ phonebook lookup 'Name'
    $ phonebook reverse-lookup 'Number'

##To-Dos

* Write tests for arg parser
* Clean up tests script
* Figure out how to get this to work on someone else's computer without them having to add a symlink on their `$PATH`
* Standardize phone number entries
* Only allow phone number args that match a regex pattern
* Allow search by partial name - trie?
* Case insensitive search
* Make names work without using quotes
* Add tab completion