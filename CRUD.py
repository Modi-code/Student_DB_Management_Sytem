import sqlite3
def createTable():
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        # cur.execute("DROP TABLE IF EXISTS users")
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL
            CHECK(NAME NOT LIKE ('%[^A-Za-z]%')),
            GRADE INTEGER NOT NULL
            CHECK (GRADE<=100 AND GRADE>=0),
            FOREIGN KEY(ID) REFERENCES auth(USER_ID)
        )
    ''')
def insert(name,grade):
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        try:
            cur.execute("INSERT INTO users(NAME,GRADE) VALUES(?,?)",(name,grade))
        except sqlite3.IntegrityError:
            print('grade out of range')
        return ('<script></script>')
def retrieve(id):
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        cur.execute("SELECT * FROM users WHERE ID=?",(id,))
        return cur.fetchall()
def update(id,grade):
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        print(cur.execute("SELECT * FROM users WHERE ID=?",(id,)).fetchall())
        try:
            cur.execute("UPDATE users SET GRADE=? WHERE ID=?",(grade,id))
        except sqlite3.IntegrityError:
            print('grade out of range')
        print('user was updated')
def delete(id):
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        cur.execute("DELETE FROM users WHERE ID=?",(id,))

def get_all():
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        cur.execute('SELECT ID,NAME,GRADE FROM users')
        result=cur.fetchall()
        return result
def get_access(id):
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        cur.execute('Select ACCESS FROM auth WHERE USER_ID=?',(id,))
        return cur.fetchone()
