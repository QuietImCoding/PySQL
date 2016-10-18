import sqlite3

database = None
c = None
location = None
initError = "You have to initialize the database first. Run db.init(*filename*)"

def init(filename):
    global database
    global c
    global location
    location = filename
    database = sqlite3.connect(filename)
    c = database.cursor()

def gettables():
    if c != None:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        stringtable = []
        for table in c.fetchall():
            stringtable.append(table[0])
        return stringtable
        

def maketable(tablename, rows):
    global c
    if c != None:
        if tablename not in  gettables():
            commandString = "CREATE TABLE %s (" % tablename
            for row in rows:
                commandString += "%s %s, " % (row, rows[row])
                commandString = commandString[:len(commandString)-2] + ")"
                print commandString
                c.execute(commandString)
        else:
            print "Table \"%s\" already exists" % tablename
    else:
        print initError

def add(tablename, items):
    global c
    if c != None:
        commandString = "INSERT INTO %s VALUES (" % tablename
        for item in items:
            commandString += item + ", "
        commandString = commandString[:len(commandString-2)] + ")"
        c.execute(commandString)
    else:
        print initError
        
