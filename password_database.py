import sqlite3
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()  # Convert to bytes and hash it

DB_NAME = 'password_database.db'

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

        # Create the table_users table 
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

    # hash the passwords
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

    mycommand = 'SELECT userid, sys_password FROM table_users WHERE sys_username = ?'
    cursor.execute(mycommand, (username,))
    results = cursor.fetchall()

    # dis-connect from the database
    db.close()

    # Check if the username exists
    if not results:
        return ["Error", "Username not found"]

    # hash the input password before comparison
    hashed_password = hash_password(password)

    # Compare the stored password (at index 0) with the hashed input password
    if results[0][1] != hashed_password:
        return ["Error", "Password incorrect"]
    else:
        return ["Success", username , results[0][0]]  # Return 'Success' and the username or user ID

def create_credential(userid, username, password, url, name):
    # connect to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    mycommand = 'INSERT INTO accounts (userID, username, password, url, app_name) VALUES(?, ?, ?, ?, ?)'
    cursor.execute(mycommand, (userid, username, password, url, name))

    # save the changes to the database
    db.commit()
    
    # dis-connect from the database
    db.close()

    
def search(userid, username, name, url):
    query = "SELECT * FROM accounts WHERE userID = ?"
    parameters = [userid]

    # Build query conditions based on provided parameters
    if username:
        query += " AND username = ?"
        parameters.append(username)

    if name:
        query += " AND app_name = ?"
        parameters.append(name)

    if url:
        query += " AND url = ?"
        parameters.append(url)

    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        
    return results  # Returns a list of tuples



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

def delete_credential(username, app_name):
    try:
        # Connect to the database
        db = sqlite3.connect(DB_NAME)
        cursor = db.cursor()

        # Prepare and execute the delete command
        cursor.execute("DELETE FROM accounts WHERE username = ? AND app_name = ?", (username, app_name))
        
        # Check if a row was deleted
        if cursor.rowcount == 0:
            print("No matching credential found to delete.")
        else:
            print(f"Deleted credential for username: {username} and app: {app_name}")

        # Save the changes
        db.commit()
    except Exception as e:
        print("Error deleting credential:", e)
    # Ensure the database connection is closed
    db.close()


if __name__ == '__main__':
    # Ensure the database is created
    #delete_database()
    
    #create_database()  # Create the tables if they don't exist
    #populatedatabase()  # Populate the tables with initial data

    # Call the function to display contents of the database
    show_all()

