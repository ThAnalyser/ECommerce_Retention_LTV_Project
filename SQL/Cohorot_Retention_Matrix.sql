USE ecommerce_retention;

-- 3a. Assign each customer to a cohort = month of first purchase
DROP TABLE IF EXISTS customer_cohort;
CREATE TABLE customer_cohort AS
SELECT
    customer_id,
    DATE_FORMAT(MIN(invoice_date), '%Y-%m-01') AS cohort_month
FROM cleaned_data
GROUP BY customer_id;

-- 3b. Every (customer, month) pair with a transaction
DROP TABLE IF EXISTS customer_activity;
CREATE TABLE customer_activity AS
SELECT DISTINCT
    cd.customer_id,
    cc.cohort_month,
    DATE_FORMAT(cd.invoice_date, '%Y-%m-01') AS activity_month
FROM cleaned_data cd
JOIN customer_cohort cc ON cd.customer_id = cc.customer_id;

-- 3c. Period number = months since cohort month
DROP TABLE IF EXISTS cohort_index;
CREATE TABLE cohort_index AS
SELECT
    customer_id,
    cohort_month,
    activity_month,
    PERIOD_DIFF(
        DATE_FORMAT(activity_month, '%Y%m'),
        DATE_FORMAT(cohort_month, '%Y%m')
    ) AS period_number
FROM customer_activity;

-- 3d. Cohort sizes
DROP TABLE IF EXISTS cohort_size;
CREATE TABLE cohort_size AS
SELECT cohort_month, COUNT(DISTINCT customer_id) AS num_customers
FROM cohort_index
WHERE period_number = 0
GROUP BY cohort_month;

-- 3e. Final retention matrix
DROP TABLE IF EXISTS cohort_retention_matrix;
CREATE TABLE cohort_retention_matrix AS
SELECT
    ci.cohort_month,
    ci.period_number,
    COUNT(DISTINCT ci.customer_id) AS retained_customers,
    cs.num_customers AS cohort_size,
    ROUND(COUNT(DISTINCT ci.customer_id) / cs.num_customers * 100, 1) AS retention_pct
FROM cohort_index ci
JOIN cohort_size cs ON ci.cohort_month = cs.cohort_month
WHERE ci.period_number BETWEEN 0 AND 11
GROUP BY ci.cohort_month, ci.period_number, cs.num_customers
ORDER BY ci.cohort_month, ci.period_number;



SELECT COUNT(*) FROM cohort_retention_matrix;
SELECT * FROM cohort_retention_matrix LIMIT 10;