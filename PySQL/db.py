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

def tables():
    if c != None:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        stringtable = []
        for table in c.fetchall():
            stringtable.append(str(table[0]))
        return stringtable
        
def columns(tablename):
    if c != None:
        c.execute("PRAGMA table_info(%s)" % tablename)
        stringdict = {}
        for tuplet in c.fetchall():
            stringdict[str(tuplet[1])] = str(tuplet[2])
        return stringdict

def create(tablename, rows):
    global c
    if c != None:
        if tablename not in tables():
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
            try:
                float(item)
                commandString += str(item) + ', '
            except ValueError:
                commandString += '"'    
                commandString += str(item) + '", '                
        commandString = commandString[:len(commandString)-2] + ")"
        c.execute(commandString)
    else:
        print initError

def close():
    database.commit()
    database.close()
