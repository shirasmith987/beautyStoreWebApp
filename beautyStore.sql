Create table customer(
cust_id int NOT NULL AUTO_INCREMENT,
last_name varchar(255) NOT NULL,
first_name varchar(255),
email  varchar(255),
address varchar(255),
PRIMARY KEY (cust_id)
)

Create table brands(
	brand_id varchar(255) NOT NULL,
	name varchar(255),
	location varchar(255),
	PRIMARY KEY (brand_id)
)

Create table product(
prod_id int NOT NULL AUTO_INCREMENT,
prod_name varchar(255) NOT NULL,
inventory int,
brand_id varchar(255),
price float,
PRIMARY KEY (prod_id),
FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
)

Create table sales(
	sale_id int NOT NULL AUTO_INCREMENT,
	cust_id int,
prod_id int,
	amount int,
date date,
    	PRIMARY KEY (sale_id),
FOREIGN KEY (cust_id) REFERENCES customer(cust_id),
FOREIGN KEY (prod_id) REFERENCES product(prod_id)
)

INSERT INTO customer(last_name, first_name, email, address) VALUES 
('Smith', 'Shira', 'shira@gmail.com', '3 Lexington Ave.' ),
('Doe', 'Jane','jane@gmail.com', '45 Third Ave.'),
('Green', 'Rachel', 'rachel@gmail.com','62 Fifth Ave.' ),
('Hunt', 'James', 'james@gmail.com', '54 Fourth St.'),
('Brown', 'Rebecca', 'rebecca@gmail.com', '43 Seventh Ave.'),
('Stern', 'Eric', 'eric@gmail.com', '23 Magnolia St.');

INSERT INTO brands(brand_id, name, location) VALUES
('Mc1', 'Mac', 'New York City, NY'),
('Dr', 'Dior', 'Paris, France'),
('LM', 'Laura Mercier', 'Paris, France'),
('UD', 'Urban Decay', 'Los Angeles, CA'),
('Clq1', 'Clinique', 'Chicago, IL'), 
('Mc2', 'MacPro', 'New York City, NY');

INSERT INTO product(prod_name, inventory, brand_id, price) VALUES
('eyeliner', 20, 'Mc1', 4.00),
('mascara', 40, 'LM', 15.00),
('eyeshadow', 33, 'Dr', 20.00),
('lipstick', 21, 'UD', 13.00),
('foundation', 12, 'Clq1', 20.00);

INSERT INTO sales(cust_id, prod_id, amount, date) VALUES 
(1, 11, 4, '2019-05-12'),
(2, 13, 2, '2019-04-11'),
(1, 12, 4, '2019-05-13'), 
(5, 14, 5, '2019-05-02'),
(6, 12, 3, '2019-04-20'), 
(4, 15, 1, '2019-05-13');

/* I believe my database is in 4nf because:
Each row is unique and each column only contains a single value
Each table doesn’t have any partial dependencies- all of the attributes of the table are relevant to that table's primary key.
There are no transitive dependencies
There are no multivalued dependencies (for my specific database, because we are only 
allowing each customer, product, and brand to have unique attributes
 - ex: no one can have many email addresses on this application).
*/
