#!/usr/bin/python3                                                                                                                                 

import cgi, cgitb
import mysql.connector

# Create instance of FieldStorage                                                                                                                  
form = cgi.FieldStorage()

# Get data from fields
if form.getvalue('product_name'):
    product_name = form.getvalue('product_name').lower().strip()
else:
    product_name = form.getvalue('product_name')
if form.getvalue('price'):
    price = form.getvalue('price').lower().strip()
else:
    price = form.getvalue('price')
if form.getvalue('inventory'):
    inventory = form.getvalue('inventory').lower().strip()
else:
    inventory = form.getvalue('inventory')
if form.getvalue('brand_name'):
    brand_name = form.getvalue('brand_name').lower().strip()
else:
    brand_name = form.getvalue('brand_name')
if form.getvalue('brand_id'):
    brand_id = form.getvalue('brand_id').lower().strip()
else:
    brand_id = form.getvalue('brand_id')
if form.getvalue('location'):
    location = form.getvalue('location').lower().strip()
else:
    location = form.getvalue('location')

#open a connection to the database
cnx = mysql.connector.connect(user='snsmith1', password='database0809',
                              host='localhost',
                              database='snsmith12')
cursor = cnx.cursor()

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>New Product Page</title>")
print("</head>")
print("<style>b {  font-size: 40px;}</style>")
print("<body>")

#check that all the necessary fields are completed
if product_name == None or price == None or inventory == None or brand_name == None or brand_id == None or location == None:
        print("""<p>You are missing information.                                                                                             
        Please go back to the <a href='../add_product.html'>previous </a>                                                                         
        page and re-insert your information.</p>""")
else:
    #check if this brand already exists in our database
        checkquery = "select * from brands where brand_id = %s"
        checkvals = (brand_id,)
        cursor.execute(checkquery, checkvals)
        row = cursor.fetchone()
        #if not, insert into DB
        if row == None:
            brandquery = "insert into brands values(%s, %s, %s)"
            brandvals = (brand_id, brand_name, location)
            cursor.execute(brandquery, brandvals)
            cnx.commit()
            productquery = "insert into product(prod_name, inventory, brand_id, price) values(%s, %s, %s, %s)"
            productvals = (product_name, inventory, brand_id, price)
            cursor.execute(productquery, productvals)
            cnx.commit()
        #else: insert only the product
        else:
            productquery = "insert into product(prod_name, inventory, brand_id, price) values(%s, %s, %s, %s)"
            productvals = (product_name, inventory, brand_id, price)
            cursor.execute(productquery, productvals)
            cnx.commit()
        #find the product id for the user to have on record
        productquery = "select * from product order by prod_id desc limit 1"
        cursor.execute(productquery)
        item = cursor.fetchone()
        productID = item[0]
        
        print("<p>Your product has been added.</p>")
        print("<p>Your product ID is <b>" + str(productID))
        print(".</b> Return to the home page <a href='../the_beauty_store.html'>here</a> and check out all of our products</p>")


print("</body>")
print("</html>")
cursor.close()
cnx.close()
