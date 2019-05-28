#!/usr/bin/python3

import cgi, cgitb
import mysql.connector 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
if form.getvalue('first_name'):
	first_name = form.getvalue('first_name').lower().strip()
else:
	first_name = form.getvalue('first_name')
if form.getvalue('last_name'):
	last_name = form.getvalue('last_name').lower().strip()
else:
	last_name = form.getvalue('last_name')
if form.getvalue('email'):
	email = form.getvalue('email').lower().strip()
else:
	email = form.getvalue('email')
if form.getvalue('address'):
	address = form.getvalue('address').lower().strip()
else:
	address = form.getvalue('address')

cnx = mysql.connector.connect(user='snsmith1', password='database0809',
                              host='localhost',
                              database='snsmith12')
cursor = cnx.cursor()

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>New Customer Page</title>")
print("</head>")
print("<body>")
print("<h2>Hello %s %s</h2>" % (first_name, last_name))
if first_name == None or last_name == None or email == None or address == None:
        print('<p>You are missing part of your name. Please return to the home page and re-insert your information.</p>')

else:
        #check if customer is already in the DB
        checkquery = "select * from customer where LOWER(first_name) = %s and LOWER(last_name) = %s"
        checkvals = (first_name, last_name,)
        cursor.execute(checkquery, checkvals)
        row = cursor.fetchone()
        #if not found, insert into the DB
        if row == None:
                query1 = "insert into customer(last_name, first_name, email, address) values (%s, %s, %s, %s)"
                val = (last_name, first_name, email, address)
                cursor.execute(query1, val)
                cnx.commit()
                print("<p>Welcome to our store! Return to the Home Page so you can start shopping!</p>")
        else:
                print('<p>You already have an account. Go back to our home page to check out our amazing products.</p>')
print("<p><a href='../the_beauty_store.html'>Return to our Home Page </a></p>")

        
print("</body>")
print("</html>")


cursor.close()
cnx.close()
