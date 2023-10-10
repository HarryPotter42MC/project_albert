import bcrypt 
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('dexify.db')
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL UNIQUE
    )
""")


#
desiredusername = input('enter your desired username: ')
password = input('enter your password: ')

try:
    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """, (desiredusername, password))
    conn.commit()
    print("User profile added to the database.")
except sqlite3.IntegrityError:
    print("A user profile with that name already exists in the database. Please choose a different name.")


#



#desiredusername = input('enter your desired username: ')
#password = input('enter your password: ')


def countuserrows():
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print("Error counting rows:", e)
        return -1  # Return -1 to indicate an error

rows_count = countuserrows()
print(rows_count)

def grabusernamesArray():
    try:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        usernames = []

        for row in rows:
            username = row["username"]
            usernames.append(username)
        
        return usernames
    except sqlite3.Error as e:
        print("Error fetching usernames")
        return[]

usernamesarray = grabusernamesArray()


def checkusernameavaiable():
    for username in usernamesarray:
        while True:
            if desiredusername == username:
                print('username available')
                return False
            else:
                print('didnt work. keep iterating')
        

            




#for name in usernamesarray:
#    print(name)




#isavailable = checkusernameavaiable(desiredusername)
#print(isavailable)


password = password.encode('utf-8')
 
hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashedPassword)