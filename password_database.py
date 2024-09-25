import sqlite3

DB_NAME = 'password_database'

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

    #populate the users table (this will not be necessary in a fully functioning system where there functionality to add users)
    cursor.execute('''
    INSERT INTO table_users(sys_username, sys_password)
    VALUES
    ('Bill','billbill'),
    ('Ben','benben');
    ''')

    #save the database
    db.commit()
    
    #dis-connect from the database
    db.close()

    #self.csvimport()
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

def userlogin(username, password):
    # connect to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    mycommand = 'SELECT * FROM table_users WHERE sys_username = ?'
    cursor.execute(mycommand, (username,))
    results = cursor.fetchall()

    # dis-connect from the database
    db.close()

    if not results:
        return ["Error", "Username not found"]
    elif results[0][2] != password:
        return ["Error", "Password incorrect"]
    else:
        return ["Success", results[0][0]]  # Return 'Success' and the 'userid'

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
    
if __name__ == '__main__':
    # Ensure the database is created
    delete_database()
    create_database()  # Create the tables if they don't exist
    populatedatabase()  # Populate the tables with initial data

    # Call the function to display contents of the database
    show_all()

