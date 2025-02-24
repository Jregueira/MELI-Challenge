-- Customer table
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
    dirección VARCHAR(200),
    fecha_nacimiento DATE,
    teléfono VARCHAR(20)
);

-- Category table
CREATE TABLE Category (
    category_id INT PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    path VARCHAR(200)
);

-- Item table
CREATE TABLE Item (
    item_id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    fecha_publicacion DATE NOT NULL,
    category_id INT,
    seller_id INT,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (seller_id) REFERENCES Customer(customer_id)
);

-- Order table
CREATE TABLE Order (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Order_Item table
CREATE TABLE Order_Item (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Order(order_id),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
); 





