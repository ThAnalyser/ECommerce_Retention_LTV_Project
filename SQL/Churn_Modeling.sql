USE ecommerce_retention;

-- 4a. Label: 1 if customer has NO transactions in last 90 days
DROP TABLE IF EXISTS churn_labels;
CREATE TABLE churn_labels AS
SELECT
    cc.customer_id,
    CASE WHEN ca.customer_id IS NULL THEN 1 ELSE 0 END AS is_churned
FROM (SELECT DISTINCT customer_id FROM cleaned_data) cc
LEFT JOIN (
    SELECT DISTINCT customer_id
    FROM cleaned_data
    WHERE invoice_date > (SELECT DATE_SUB(MAX(invoice_date), INTERVAL 90 DAY) FROM cleaned_data)
) ca ON cc.customer_id = ca.customer_id;

-- 4b. Features from BEFORE the holdout window
DROP TABLE IF EXISTS churn_features;
CREATE TABLE churn_features AS
SELECT
    customer_id,
    DATEDIFF(
        (SELECT DATE_SUB(MAX(invoice_date), INTERVAL 90 DAY) FROM cleaned_data),
        MAX(invoice_date)
    ) AS recency,
    COUNT(DISTINCT invoice) AS frequency,
    ROUND(SUM(line_total), 2) AS monetary,
    ROUND(SUM(line_total) / COUNT(DISTINCT invoice), 2) AS avg_order_value,
    COUNT(DISTINCT stock_code) AS unique_products
FROM cleaned_data
WHERE invoice_date <= (SELECT DATE_SUB(MAX(invoice_date), INTERVAL 90 DAY) FROM cleaned_data)
GROUP BY customer_id;

-- 4c. Final modeling table
DROP TABLE IF EXISTS churn_modeling_data;
CREATE TABLE churn_modeling_data AS
SELECT f.*, l.is_churned
FROM churn_features f
JOIN churn_labels l ON f.customer_id = l.customer_id;

USE ecommerce_retention;

SELECT COUNT(*) FROM churn_modeling_data;
SELECT is_churned, COUNT(*) FROM churn_modeling_data GROUP BY is_churned;