USE ecommerce_retention;

-- =========================================================
-- STEP 1: CLEANING
-- Removes: blank CustomerIDs, cancellations, bad quantities/prices
-- Casts:  strings → proper types
-- =========================================================
DROP TABLE IF EXISTS cleaned_data;
CREATE TABLE cleaned_data AS
SELECT
    Invoice                                      AS invoice,
    StockCode                                      AS stock_code,
    Description                                    AS description,
    CAST(Quantity AS UNSIGNED)                     AS quantity,
    STR_TO_DATE(InvoiceDate, '%m/%d/%Y %H:%i')     AS invoice_date,
    CAST(Price AS DECIMAL(10,2))                   AS price,
    CAST(CustomerID AS UNSIGNED)                   AS customer_id,
    Country                                        AS country,
    (CAST(Quantity AS UNSIGNED) * CAST(Price AS DECIMAL(10,2))) AS line_total
FROM online_retail_II_raw
WHERE CustomerID IS NOT NULL
  AND CustomerID != ''
  AND CustomerID != '0'
  AND Invoice NOT LIKE 'C%'
  AND CAST(Quantity AS SIGNED) > 0
  AND CAST(Price AS DECIMAL(10,2)) > 0;

