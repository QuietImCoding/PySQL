import sqlite3
import collections
import random
from Crypto.Cipher import AES

database = None
c = None
location = None
initError = "You have to initialize the database first. Run db.init(*filename*)"

def scramble(filename):
    datafile = open("data.db", "r")
    blub = datafile.read()
    datafile.close()
    
    key = b''
    for i in range(0,16):
        key+=str(random.randint(0,9))
        
    print key
        
    cipher = AES.new(key)
        
    blub = cipher.encrypt(blub)
    
    datafile = open("data.db", "w")
    datafile.write(blub)
    datafile.close()
    
def unscramble(filename):
    datafile = open(filename, 'r')
    blub = datafile.read()
    datafile.close()
    
    key = raw_input("Key: ")
    cipher = AES.new(key)
    
    blub = cipher.decrypt(blub)
    
    datafile = open(filename, 'w')
    datafile.write(blub)
    datafile.close()
        
#Also important
def init(filename="data.db"):
    global database
    global c
    global location
    location = filename
    database = sqlite3.connect(filename)
    c = database.cursor()
    try:
        c.execute("PRAGMA schema_version")
    except sqlite3.DatabaseError:
        descramble(filename)
        

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
        stringdict = collections.OrderedDict()
        for tuplet in c.fetchall():
            stringdict[str(tuplet[1])] = str(tuplet[2])
        return stringdict

def select(tablename, rows, where=""):
    if c != None:
        commandString = "SELECT "
        for row in rows:
            commandString += "%s, " % row
        commandString = commandString[:len(commandString)-2]
        commandString += " FROM %s" % tablename
        if where != "":
            commandString+=" WHERE %s" % where
        print commandString
        c.execute(commandString)
        return c.fetchall()
    else:
        print initError    
    
def create(tablename, rows):
    global c
    if c != None:
        if tablename not in tables():
            commandString = "CREATE TABLE %s (" % tablename
            for row in rows:
                commandString += "%s %s, " % (row, rows[row])
            commandString = commandString[:len(commandString)-2] + ")"
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

#Important
def close():
    database.commit()
    database.close()
