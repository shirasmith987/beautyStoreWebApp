#!/usr/bin/python3                                                                                                                                       

import cgi, cgitb
import mysql.connector
import datetime

# Create instance of FieldStorage                                                                                                                        
form = cgi.FieldStorage()

# Get data from fields                                                                                                                                   
if form.getvalue('saleID'):
        saleID = form.getvalue('saleID').lower().strip()
else:
        saleID = form.getvalue('saleID')
if form.getvalue('quantity'):
        quantity = form.getvalue('quantity').lower().strip()
else:
        quantity = form.getvalue('quantity')
        
cnx = mysql.connector.connect(user='snsmith1', password='database0809',
                              host='localhost',
                              database='snsmith12')
cursor = cnx.cursor()

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Return Product CGI Page</title>")
print("</head>")
print("<body>")

#makes sure sale id is inputted
if saleID == None:
        print('''<p>You must enter your sale ID number.
        Please return to the <a href="../return_item.html">previous </a> page.
        If you cannot find your sale ID number, please call customer service.</p>''')
else:
        checkquery = "select * from sales where sale_id = %s"
        checkvals = (saleID,)
        cursor.execute(checkquery, checkvals)
        row = cursor.fetchone()
        #checks this sale is recorded in DB
        if row == None:
                print("""<p>We can't find your sale in our system. Check that you have the correct sale ID
                You can return to the <a href='../return_item.html'>previous </a> 
                page here and try again.</p>""")
        else:
                amount = int(row[3])
                quantity = int(quantity)
                #returns part of an order (updates sale table)
                if quantity:
                        quantity = int(quantity)
                        #checks the amount to be returned is less than the amount purchased
                        if  quantity > amount:
                                print("""<p>You can't return more than you purchased.
                                Return to the home page <a href='../the_beauty_store'>here</a>.</p>""") 
                        else:
                                prod_id = row[2]
                                salesquery = "update sales set amount= amount - %s where sale_id = %s"
                                salesval = (quantity, saleID)
                                cursor.execute(salesquery, salesval)
                                cnx.commit()
                                prodquery = "update product set inventory = inventory+%s where prod_id = %s"
                                prodvals = (quantity, prod_id)
                                cursor.execute(prodquery, prodvals)
                                cnx.commit()
                                print("<p>Your purchase has been returned. Return to the home page <a href='../the_beauty_store'>here</a>.</p>")

                #deletes entire sale record from DB, and updates product inventory to reflect return
                else:
                        amount = row[3]
                        prod_id = row[2]
                        salesquery = "delete from sales where sale_id = %s"
                        salesval = (saleID,)
                        cursor.execute(salesquery, salesval)
                        cnx.commit()
                        prodquery = "update product set inventory = inventory+%s where prod_id = %s"
                        prodvals = (amount, prod_id)
                        cursor.execute(prodquery, prodvals)
                        cnx.commit()
                        print("<p>Your purchase has been returned. Return to the home page <a href='../the_beauty_store'>here</a>.</p>")
print("</body>")
print("</html>")


cursor.close()
cnx.close()
