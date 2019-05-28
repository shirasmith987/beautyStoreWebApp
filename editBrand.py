#!/usr/bin/python3                                                                                                                       
import cgi, cgitb
import mysql.connector

# Create instance of FieldStorage                                                                                                 
form = cgi.FieldStorage()

# Get data from fields                                                                                                                         
if form.getvalue('brand_id'):
        brand_id = form.getvalue('brand_id').lower().strip()
else:
        brand_id = form.getvalue('brand_id')
if form.getvalue('location'):
        location = form.getvalue('location').lower().strip()
else:
        location = form.getvalue('location')
if form.getvalue('prod_id'):
        prod_id = form.getvalue('prod_id').lower().strip()
else:
        prod_id = form.getvalue('prod_id')
if form.getvalue('delete_brand'):
        delete_brand = form.getvalue('delete_brand').lower().strip()
else:
        delete_brand = form.getvalue('delete_brand')

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

#check all fields are filled out
if (brand_id == None or location == None) and (delete_brand == None) and (prod_id == None):
        print("""<p>You must fill in one of the sections.
        Please go back to the <a href='../edit_product.html'>previous </a> page and re-insert your information.</p>""")
else:
        #if brand and location is set, update brand's location
        if brand_id and location:
                checkquery = "select * from brands where brand_id = %s"
                checkvals = (brand_id,)
                cursor.execute(checkquery, checkvals)
                row = cursor.fetchone()
                if row == None:
                        print("""<p>We don't have record of your brand in our system.
                        Return to our home page <a href='../the_beauty_store.html'>here.</a></p>""")
                else:
                        updateBrand = "update brands set location= %s where brand_id = %s"
                        updatevals = (location, brand_id)
                        cursor.execute(updateBrand, updatevals)
                        cnx.commit()
                        print("""<p>Your brand's location has been updated.
                        You can return to the <a href='../the_beauty_store.html'>home </a> page.</p>""")
#if delete brand is set, delete brand
        if delete_brand:
                checkquery = "select * from brands where brand_id = %s"
                checkvals = (delete_brand,)
                cursor.execute(checkquery, checkvals)
                row = cursor.fetchone()
                if row == None:
                        print("""<p>We don't have record of your brand in our system.                                                           
                        Return to our home page <a href='../the_beauty_store.html'>here.</a></p>""")
                else:
                        checkquery = "select * from product where brand_id = %s"
                        checkvals = (delete_brand,)
                        cursor.execute(checkquery, checkvals)
                        row = cursor.fetchone()
                        if row:
                                print("""<p>We cannot delete your brand since we still have products from your
                                brand in our inventory.                                                     
                                Return to our home page <a href='../the_beauty_store.html'>here.</a></p>""")
                        else:
                                deleteBrand = "delete from brands where brand_id = %s"
                                deletevals = (delete_brand,)
                                cursor.execute(deleteBrand, deletevals)
                                cnx.commit()
                                print("""<p>Your brand has been has been deleted.
                                You can return to the <a href='../the_beauty_store.html'>home </a> page.</p>""")
#delete product
        if prod_id:
                checkquery = "select * from product where prod_id = %s"
                checkvals = (prod_id,)
                cursor.execute(checkquery, checkvals)
                row = cursor.fetchone()
                if row == None:
                        print("""<p>We don't have record of your product in our system.                             
                        Return to our home page <a href='../the_beauty_store.html'>here.</a></p>""")
                else:
                        checkquery = "select * from sales where prod_id = %s"
                        checkvals = (prod_id,)
                        cursor.execute(checkquery, checkvals)
                        row = cursor.fetchone()
                        if row:
                                print("""<p>We cannot delete your product since we have already made sales                                  
                                 of your product.                                                                                           
                                Return to our home page <a href='../the_beauty_store.html'>here.</a></p>""")
                        else:
                                deleteprod = "delete from product where prod_id = %s"
                                deletevals = (prod_id,)
                                cursor.execute(deleteprod, deletevals)
                                cnx.commit()
                                print("""<p>Your product has been has been deleted.                                            
                                You can return to the <a href='../the_beauty_store.html'>home </a> page.</p>""")


print("</body>")
print("</html>")
cursor.close()
cnx.close()
