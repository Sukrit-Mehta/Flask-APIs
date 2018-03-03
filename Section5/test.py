import sqlite3   

connection = sqlite3.connect("data.db") #sql stores data in a file which we hav named data.db

cursor = connection.cursor() # cursor allows you to select things ad store the results.

#to create a table in sql

create_table = "CREATE TABLE users (id int, username text, password text)"

#to run the query

cursor.execute(create_table)

#inserting single user

user = (1,'sukrit','asdf') #tuple

insert_query = "INSERT INTO users VALUES(?, ?, ?)"

cursor.execute(insert_query,user)


# inserting multiple users

users = [
			(2,'sarthak','asdf'),
			(3,'abhay','asdf')
		]

cursor.executemany(insert_query,users)

# retrieve data from table

select_query = "SELECT * from users"

for row in cursor.execute(select_query):
	print(row)

#save the changes in db file

connection.commit()

connection.close()