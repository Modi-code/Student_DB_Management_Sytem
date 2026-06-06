import hashlib, os, sqlite3
def create_auth_table():
    with sqlite3.connect('data') as con:
        cur =con.cursor()
        cur.execute('DROP TABLE IF EXISTS auth')
        cur.execute('''
                CREATE TABLE IF NOT EXISTS auth(
                USER_ID VARCHAR(200) NOT NULL PRIMARY KEY
                CHECK(USER_ID NOT LIKE ('%[^A-Za-z]%')),
                PASSWORD CHAR(32) NOT NULL,
                SALT CHAR(16) NOT NULL,
                ACCESS VARCHAR(30) NOT NULL DEFAULT 'STUDENT'
                )
        ''')
        con.commit()

def encrypt(password,salt=None):
    if salt is None:
        salt = os.urandom(16)
    password=password.encode('utf-8')
    hashed=hashlib.scrypt(password,salt=salt,n=16384,r=8,p=1,dklen=32)
    return hashed.hex(),salt

def userid_exists(user_id):
    with sqlite3.connect('data') as conn:
        cur =conn.cursor()
        cur.execute("SELECT COUNT(*) FROM auth WHERE USER_ID=?",(user_id,))
        result=cur.fetchone()[0]
        return True if result > 0 else False

def account_exists(user_id,password):
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        cur.execute("SELECT PASSWORD,SALT FROM auth WHERE USER_ID=?",(user_id,))
        result=cur.fetchone()
        if result == None:
            return False
        encryption=encrypt(password,result[1])[0]
        if encryption==result[0]:
            return True
        else:
            return False
def new_account(user_id,password):
    with sqlite3.connect('data') as con:
        cur=con.cursor()
        encrypted,salt=encrypt(password)
        cur.execute('INSERT INTO auth(USER_ID, PASSWORD, SALT) VALUES(?,?,?)',(user_id,encrypted,salt))
        con.commit()
