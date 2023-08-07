CREATE TABLE IF NOT EXISTS drogasil (

    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    sku INT,
    EAN BIGINT,
    product VARCHAR(255),
    brand VARCHAR(255),
    quantity VARCHAR(10),
    weight FLOAT,
    manufacturer VARCHAR(255),
    description TEXT,
    category VARCHAR(255),
    sub_category VARCHAR(255)

);