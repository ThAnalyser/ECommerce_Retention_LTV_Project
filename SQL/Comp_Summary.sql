USE ecommerce_retention;

-- Customers: one row per customer
DROP TABLE IF EXISTS customers;
CREATE TABLE customers AS
SELECT customer_id, country
FROM (
    SELECT customer_id, country,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY COUNT(*) DESC) AS rn
    FROM cleaned_data
    GROUP BY customer_id, country
) ranked
WHERE rn = 1;

-- Products: one row per stock_code
DROP TABLE IF EXISTS products;
CREATE TABLE products AS
SELECT stock_code, description
FROM (
    SELECT stock_code, description,
           ROW_NUMBER() OVER (PARTITION BY stock_code ORDER BY COUNT(*) DESC) AS rn
    FROM cleaned_data
    GROUP BY stock_code, description
) ranked
WHERE rn = 1;

-- Orders: one row per invoice
DROP TABLE IF EXISTS orders;
CREATE TABLE orders AS
SELECT invoice, customer_id, MIN(invoice_date) AS invoice_date
FROM cleaned_data
GROUP BY invoice, customer_id;

-- Order items
DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items AS
SELECT invoice, stock_code, quantity, price, line_total
FROM cleaned_data;

USE ecommerce_retention;

SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM order_items;