CREATE TABLE IF NOT EXISTS drogasil (

    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    url varchar(255),
    sku int,
    EAN int,
    product varchar(255),
    brand varchar(255),
    quantity int,
    weight float,
    manufacturer varchar(255),
    description text,
    category varchar(255),
    sub_category varchar(255),
    price decimal(10, 2),
    discount int

);