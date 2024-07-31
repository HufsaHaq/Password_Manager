import psycopg2

DB_NAME = 'password_database'
DB_USER = 'postgres'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '5432'

def delete_database():
    # connect to the database
    db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
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
        db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = db.cursor()

        # Create the accounts table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            userID SERIAL,
            username TEXT NOT NULL,
            password TEXT NOT NULL, 
            url TEXT NOT NULL, 
            app_name TEXT NOT NULL
        );''')

        #create user table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS table_users(
        userID SERIAL PRIMARY KEY,
        sys_username VARCHAR(20) NOT NULL,
        sys_password VARCHAR(20) NOT NULL);
        ''')
    
        # Save changes and close the database
        db.commit()
        db.close()

        print("Database created successfully")
    except psycopg2.Error as e:
        print("Error:", e)

def populatedatabase():

    print("Running populatedatabase")

    # connect to the database
    db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
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
    db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
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
    db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    cursor = db.cursor()

    mycommand = 'SELECT * FROM table_users WHERE sys_username = %s'
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

def create_password(userid,username,password,url,name):
    # connect to the database
    db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    cursor = db.cursor()
    mycommand = 'INSERT INTO accounts (userID,username,password, url, app_name) VALUES(%s,%s,%s,%s,%s)'
    cursor.execute(mycommand,(userid,username,password,url,name,))

    #dis-connect from the database
    db.close()
    
def search(userid,username,password,url,name):
    # connect to the database
    db = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
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
        query += " AND name = ?"
        query_params.append(name)
       
    cursor.execute(query, query_params)

    #dis-connect from the database
    db.close()
    
if __name__ == '__main__':
    # Call the function to delete the database
    #delete_database()
    
    # Call the function to create the database and tables
    #create_database()
    #populatedatabase()

    # Call the function to display contents of the database
    show_all()
