#!/usr/bin/python3                                                           

import cgi, cgitb
import mysql.connector

# Create instance of FieldStorage                                            
form = cgi.FieldStorage()
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Products Page</title>")
print("</head>")
print("<style>table, th, td {  border: 1px solid black;  border-collapse: collapse;}</style>")
print("<body>")
cnx = mysql.connector.connect(user='snsmith1', password='database0809',
                              host='localhost',
                              database='snsmith12')
cursor = cnx.cursor()
#this form displays all of our products in the format requested by the user
if form.getvalue('products') or form.getvalue('brands'):
    #displays in order of products
    if form.getvalue('products'):
        productquery = "select * from product p, brands b where p.brand_id = b.brand_id order by p.prod_name"
        cursor.execute(productquery)
        #creates a table to view products
        print('<table>')
        print('<tr><th>Product Name</th><th>Price</th><th>Brand</th><th>Product ID</th></tr>')
        for i in cursor:
            print('<tr>')
            print('<td>' + str(i[1]) + '</td>')
            amountLeft = i[2]
            if amountLeft  == 0:
                print('<td> $' + str(i[4]) + ' (SOLD OUT)</td>')
            else:
                print('<td> $' + str(i[4]) + '</td>')
            print('<td>' + str(i[6]) + '</td>')
            print('<td>' + str(i[0]) + '</td>')
            print('</tr>')
        print('</table>')
    #displays by brand name
    elif form.getvalue('brands'):
        productquery = "select * from product p, brands b where p.brand_id = b.brand_id order by p.brand_id"
        cursor.execute(productquery)
        print('<table>')
        print('<tr><th>Brand</th><th>Product Name</th><th>Price</th><th>Product ID</th></tr>')
        for i in cursor:
            print('<tr>')
            print('<td>' + str(i[6]) + '</td>')
            print('<td>' + str(i[1]) + '</td>')
            amountLeft = i[2]
            if amountLeft  == 0:
                print('<td> $' + str(i[4]) + ' (SOLD OUT)</td>')
            else:
                print('<td> $' + str(i[4]) + '</td>')
            print('<td>' + str(i[0]) + '</td>')
            print('</tr>')
        print('</table>')
    #this form processes purchases
    print("<p>If you would like to make a purchase, please enter you first and last name as well as the Product ID number and amount you would like to purchase</p>")
    print("""<form action='processPurchase.py' method='post'>
     First Name <input type = 'text' name = 'first_name'><br />
     Last Name <input type = 'text' name = 'last_name'><br />
     Product ID <input type = 'text' name = 'prod_id'><br />
     Quantity <input type = 'text' name = 'amount'><br />
     <input type = 'submit' value = 'Submit'/></form>""")
else:
    print("<p>You forgot to choose an option. Click <a href='../returning_customer_page.html'>here</a> to return to the previous page.</p>")
                                                                                    
print("</body>")
print("</html>")

cursor.close()
cnx.close()
