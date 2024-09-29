import sqlite3
from hashlib import sha256


DB_NAME = 'password_database.db'

def hash_password(password):
    return sha256(password.encode()).hexdigest()  # Convert to bytes and hash it

##############################################################################################################

def delete_database():
    # connect to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    cursor.execute('''DROP TABLE IF EXISTS accounts;''')
    cursor.execute('''DROP TABLE IF EXISTS table_users;''')
    print("Tables deleted")

    #save the database
    db.commit()  

    #dis-connect from the database
    db.close()
  
def create_database():
    try:
        # connect to the database
        db = sqlite3.connect(DB_NAME)
        cursor = db.cursor()

        # Create the accounts table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL, 
            url TEXT NOT NULL, 
            app_name TEXT NOT NULL
        );''')

        # Create the table_users table (fixed the issue with duplicate PRIMARY KEY)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS table_users(
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            sys_username VARCHAR(20) NOT NULL,
            sys_password VARCHAR(20) NOT NULL
        );
        ''')

        # Save changes and close the database
        db.commit()
        db.close()

        print("Database created successfully")
    except Exception as e:
        print("Error:", e)

def populatedatabase():
    print("Running populatedatabase")

    # connect to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    # Hash the passwords
    hashed_password_bill = hash_password("billbill")
    hashed_password_ben = hash_password("benben")

    # populate the users table
    cursor.execute('INSERT INTO table_users(sys_username, sys_password) VALUES (?, ?)', ('Bill', hashed_password_bill))
    cursor.execute('INSERT INTO table_users(sys_username, sys_password) VALUES (?, ?)', ('Ben', hashed_password_ben))

    # save the database
    db.commit()

    # dis-connect from the database
    db.close()

    print("Populated the database")
    
def show_all():
    # connect to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    
    # show the entries in the accounts table
    print("ACCOUNTS TABLE")
    cursor.execute("SELECT * FROM accounts")
    results = cursor.fetchall()
    for i in results:
        print(i)

    # show the entries in the users table
    print("USERS TABLE")
    cursor.execute("SELECT * FROM table_users")
    results = cursor.fetchall()
    for i in results:
        print(i)
###################################################################################################################
def userlogin(username, password):
    # connect to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    mycommand = 'SELECT sys_password FROM table_users WHERE sys_username = ?'
    cursor.execute(mycommand, (username,))
    results = cursor.fetchall()

    # dis-connect from the database
    db.close()

    # Check if the username exists
    if not results:
        return ["Error", "Username not found"]

    # Hash the input password before comparison
    hashed_password = hash_password(password)

    # Compare the stored password (at index 0) with the hashed input password
    if results[0][0] != hashed_password:
        return ["Error", "Password incorrect"]
    else:
        return ["Success", username]  # Return 'Success' and the username or user ID

def create_password(userid, username, password, url, name):
    # connect to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    mycommand = 'INSERT INTO accounts (userID, username, password, url, app_name) VALUES(?, ?, ?, ?, ?)'
    cursor.execute(mycommand, (userid, username, password, url, name))

    # save the changes to the database
    db.commit()
    
    # dis-connect from the database
    db.close()

    
def search(userid,username,password,url,name):
    # connect to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    query = "SELECT * FROM accounts WHERE 1 = 1 "

    query_params = []

    # Modify the conditions to exclude empty strings
    if userid and userid != '*':
        query += " AND userid = ?"
        query_params.append(userid)
    if username and username != '*':
        query += " AND username = ?"
        query_params.append(username)
    if password and password != '*':
        query += " AND password = ?"
        query_params.append(password)
    if url and url != '*':
        query += " AND url = ?"
        query_params.append(url)
    if name and name != '*':
        query += " AND app_name = ?"
        query_params.append(name)

       
    cursor.execute(query, query_params)
    results = cursor.fetchall()
    
    #dis-connect from the database
    db.close()

def search_password(userid, username, password):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    query = "SELECT username, password, url, app_name FROM accounts WHERE 1=1"
    query_params = []

    if userid and userid != '*':
        query += " AND userID = ?"
        query_params.append(userid)
    if username and username != '*':
        query += " AND username = ?"
        query_params.append(username)
    if password and password != '*':
        query += " AND password = ?"
        query_params.append(password)

    cursor.execute(query, query_params)
    results = cursor.fetchall()
    
    db.close()

    # Return first matching result, or None
    if results:
        return results[0]
    return None


def create_user(username, hashed_password):
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    try:
        cursor.execute('INSERT INTO table_users(sys_username, sys_password) VALUES (?, ?)', (username, hashed_password))
        db.commit()
    except sqlite3.IntegrityError as e:
        print("Error creating user:", e)
        raise e
    finally:
        db.close()

if __name__ == '__main__':
    # Ensure the database is created
    #delete_database()
    
    #create_database()  # Create the tables if they don't exist
    #populatedatabase()  # Populate the tables with initial data

    # Call the function to display contents of the database
    show_all()

