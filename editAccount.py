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

#check fields are filled out
if first_name == None or last_name == None:
        print("""<p>You are missing part of your name.
        Please go back to the <a href='../edit_account.html'>previous </a>
        page and re-insert your information.</p>""")
else:
    #find this user
        checkquery = "select * from customer where LOWER(first_name) = %s and LOWER(last_name) = %s"
        checkvals = (first_name, last_name,)
        cursor.execute(checkquery, checkvals)
        row = cursor.fetchone()
        #if not found
        if row == None:
                 print("""<p>We don't have record of your account in our system.
                 Return to our home page <a href='../the_beauty_store.html'>here.</a></p>""")
        #else, update email or address as requested
        else:
                cust_id = int(row[0])
                for i in cursor:
                    a = i
                if email:
                    emailquery = "update customer set email=%s where cust_id=%s"
                    emailvals = (email, cust_id)
                    cursor.execute(emailquery, emailvals)
                    cnx.commit()
                if address:
                    addressquery = "update customer set address=%s where cust_id=%s"
                    addressvals= (address, cust_id)
                    cursor.execute(addressquery, addressvals)
                    cnx.commit()
                print("<p>Your account has been updated. Return to the home page <a href='../the_beauty_store.html'>here</a>.</p>")

print("</body>")
print("</html>")
cursor.close()
cnx.close()
