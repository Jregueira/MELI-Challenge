-- 1. Usuarios que cumplen años hoy con ventas > 1500 en enero 2020

SELECT DISTINCT 
    c.customer_id,
    c.nombre,
    c.apellido,
    c.fecha_nacimiento
FROM Customer c
INNER JOIN Item i ON i.seller_id = c.customer_id
INNER JOIN Order_Item oi ON oi.item_id = i.item_id
INNER JOIN "Order" o ON o.order_id = oi.order_id
WHERE 
    EXTRACT(MONTH FROM c.fecha_nacimiento) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(DAY FROM c.fecha_nacimiento) = EXTRACT(DAY FROM CURRENT_DATE)
    AND EXTRACT(MONTH FROM o.order_date) = 1
    AND EXTRACT(YEAR FROM o.order_date) = 2020
GROUP BY c.customer_id, c.nombre, c.apellido, c.fecha_nacimiento
HAVING SUM(oi.quantity * oi.unit_price) > 1500;

-- 2. Top 5 vendedores de Celulares por mes en 2020
SELECT 
    EXTRACT(YEAR FROM o.order_date) as año,
    EXTRACT(MONTH FROM o.order_date) as mes,
    c.nombre,
    c.apellido,
    COUNT(DISTINCT o.order_id) as cantidad_ventas,
    SUM(oi.quantity) as cantidad_productos,
    SUM(oi.quantity * oi.unit_price) as monto_total
FROM Customer c
INNER JOIN Item i ON i.seller_id = c.customer_id
INNER JOIN Order_Item oi ON oi.item_id = i.item_id
INNER JOIN "Order" o ON o.order_id = oi.order_id
INNER JOIN Category cat ON cat.category_id = i.category_id
WHERE 
    EXTRACT(YEAR FROM o.order_date) = 2020
    AND cat.descripcion = 'Celulares'
GROUP BY 
    EXTRACT(YEAR FROM o.order_date),
    EXTRACT(MONTH FROM o.order_date),
    c.customer_id,
    c.nombre,
    c.apellido
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY EXTRACT(YEAR FROM o.order_date), EXTRACT(MONTH FROM o.order_date)
    ORDER BY SUM(oi.quantity * oi.unit_price) DESC
) <= 5
ORDER BY 
    año,
    mes,
    monto_total DESC;

-- 3. Crear y poblar tabla de histórico de precios y estados
-- Primero creamos la tabla
CREATE TABLE Item_History (
    item_id INT,
    precio DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP NOT NULL,
    PRIMARY KEY (item_id, fecha_registro),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

-- Creamos el Stored Procedure para poblar la tabla
CREATE OR REPLACE PROCEDURE SP_Populate_Item_History()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insertamos el registro del día actual
    INSERT INTO Item_History (item_id, precio, estado, fecha_registro)
    SELECT 
        item_id,
        precio,
        estado,
        CURRENT_DATE
        
    FROM Item i
    WHERE NOT EXISTS (
        SELECT 1 
        FROM Item_History ih 
        WHERE ih.item_id = i.item_id 
        AND DATE(ih.fecha_registro) = CURRENT_DATE
    );
    
    COMMIT;
END;
$$;

-- Ejecutar el SP (esto debería programarse para correr al final del día)
CALL SP_Populate_Item_History(); 