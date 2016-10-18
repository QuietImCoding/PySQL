# PySQL
A simplified sql module based on sqlite3

## How to Use

### How to import  

* from PySQL import db
* then you have access to all of the db commands

### Commands  

* the first command you always want to run is db.init(*filename*)
* the last command you run is db.close() because if you don't the database won't save and you will be left sad
* Other commands are:
	- tables() : returns a list of all the tables in the database
	- columns(String tablename) : returns a dictionary of all the fields in a database and their types
	- create(String tablename, dict rows) : creates a table with name tablename and uses the rows dict for field names. Format should be { "namea" : "TYPE", "nameb" : "TYPE" etc.... }
	- add(String tablename, List items): inserts all of the items in the items list into table tablename
