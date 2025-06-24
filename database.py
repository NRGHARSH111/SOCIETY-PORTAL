import sqlite3

con=sqlite3.connect("portal.db")
c=con.cursor()



# c.execute("create table student(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,email TEXT,password TEXT,contact INTEGER")
# c.execute("create table profile(id integer PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT, contact INTEGER, address Varchar(20))")
# c.execute("DROP TABLE profile")

# c.execute("create table login(id integer PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)")
# c.execute("INSERT INTO login(email, password) VALUES (?, ?)", ("harsh@gmail.com", "1234"))


# c.execute("create table maintainence(id integer PRIMARY KEY AUTOINCREMENT, flat TEXT, name TEXT,month TEXT,status TEXT,date TEXT)")


# c.execute("DELETE FROM maintainence")
# c.execute(" create table expenses( id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL, amount INTEGER NOT NULL,date TEXT NOT NULL, status TEXT CHECK(status IN ('Paid', 'Pending')) NOT NULL)")
# c.execute("ALTER TABLE maintainence ADD COLUMN amount INTEGER")


# c.execute("ALTER TABLE expenses ADD COLUMN month TEXT")
  
# c.execute("DELETE FROM maintainence")
# c.execute("DELETE FROM expenses")


# c.execute(" create table profile( id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT,  email TEXT ,firstname TEXT , lastname TEXT,contact INTEGER)")


# c.execute("INSERT INTO profile(fullname,email,firstname,lastname,contact ) VALUES (?,?,?,?, ?)", ("harsh kadam","harsh@gmail.com", "harsh","kadam",8421461752))

c.execute("DELETE FROM entries")






con.commit()
con.close()