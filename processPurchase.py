#!/usr/bin/python3                                                                                                                                 

import cgi, cgitb
import mysql.connector
import datetime

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
if form.getvalue('prod_id'):
        prod_id = form.getvalue('prod_id').lower().strip()
else:
        prod_id = form.getvalue('prod_id')
if form.getvalue('amount'):
        amount = form.getvalue('amount').lower().strip()
else:
        amount = form.getvalue('amount')
		
cnx = mysql.connector.connect(user='snsmith1', password='database0809',
                              host='localhost',
                              database='snsmith12')
cursor = cnx.cursor()

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>New Customer Page</title>")
print("</head>")
print("<style>b {  font-size: 40px;}</style>")
print("<body>")
#check necessary fields are filled
if first_name == None or last_name == None or amount == None or prod_id == None:
        print('<p>You are missing some necessary information. Please return to the <a href="../returning_customer_page.html">previous </a> page and re-insert your information.</p>')
else:
        #find customer
        checkquery = "select * from customer where LOWER(first_name) = %s and LOWER(last_name) = %s"
        checkvals = (first_name, last_name,)
        cursor.execute(checkquery, checkvals)
        row = cursor.fetchone()
        if row == None:
                print("""<p>We don't have record of your account in our system.
                Please return to the <a href='../returning_customer_page.html'>previous </a>
                page and re-insert your information.</p>""")
        else:
                #find product id, amount and date
                email = row[3]
                cust_id = int(row[0])
                checkquery = "select * from product where prod_id= %s"
                checkvals = (prod_id,)
                cursor.execute(checkquery, checkvals)
                row = cursor.fetchone()
                amount = int(amount)
                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d")
                #make sure we have that product
                if row == None:
                        print("<p>We don't have a product with that ID number in our system. Please return to the <a href='../returning_customer_page.html'>previous </a> page and re-insert your information.</p>")
                #make sure we have enough of that product
                elif amount > row[2]:
                        print("<p>We are so sorry, but we do not have enough in stock. Please return to the <a href='../returning_customer_page.html'>previous </a> page.</p>")
                #insert sale into DB, and update inventory to reflect sale
                else:
                        salesquery = "insert into sales(cust_id, prod_id, amount, date) values (%s, %s, %s, %s)"
                        salesval = (cust_id, prod_id, amount, date)
                        cursor.execute(salesquery, salesval)
                        cnx.commit()
                        prodquery = "update product set inventory = inventory-%s where prod_id = %s and inventory > 0"
                        prodvals = (amount, prod_id)
                        cursor.execute(prodquery, prodvals)
                        cnx.commit()
                        #return order number in case of returns
                        squery = "select * from sales order by sale_id desc limit 1"
                        cursor.execute(squery)
                        row = cursor.fetchone()
                        saleID = row[0]
                        print("<p>Thank you for shopping with us! </p>")
                        print("<p>Your sale ID number is <b>" + str(saleID) + "</b>. Hold onto this ID if you would like to make a return.</p>")
                        print("<p>We will send an email confirmation to " + email + " where you can complete your purchase.</p>")
                        print("<p>We hope you come back soon! You can click <a href='../returning_customer_page.html'> here </a> to make another purchase.</p>")
print("</body>")
print("</html>")


cursor.close()
cnx.close()
