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

#open a connection to the database 
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

#make sure the necessary fields are completed
if first_name == None or last_name == None:
        print("<p>You are missing part of your name. Please go back to the <a href='../delete_account.html'>previous </a> page and re-insert your information.</p>")

else:
        #check if the user is in the system
	checkquery = "select * from customer where LOWER(first_name) = %s and LOWER(last_name) = %s"
	checkvals = (first_name, last_name,)
	cursor.execute(checkquery, checkvals)
	row = cursor.fetchone()
	if row == None:
		 print("<p>We don't have record of your account in our system. Return to our home page <a href='../the_beauty_store.html'>here.</a></p>")
	else:
                #delete the user's account and sales and
                cust_id = int(row[0])
                for i in cursor:
                        a = i
                deleteSales = "delete from sales where cust_id=%s"
                deletevals = (cust_id,)
                cursor.execute(deleteSales, deletevals)
                cnx.commit()
                deleteCust = "delete from customer where cust_id=%s"
                cursor.execute(deleteCust, deletevals)
                cnx.commit()
                print("<p>Your account has been deleted. We hope you will come back soon!</p>")
                
print("</body>")
print("</html>")
cursor.close()
cnx.close()
