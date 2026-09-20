USE ecommerce_retention;

-- =========================================================
-- STEP 2: RFM SUMMARY
-- =========================================================
DROP TABLE IF EXISTS rfm_summary;
CREATE TABLE rfm_summary AS
SELECT
    customer_id,
    DATEDIFF(
        (SELECT DATE_ADD(MAX(invoice_date), INTERVAL 1 DAY) FROM cleaned_data),
        MAX(invoice_date)
    ) AS recency,
    COUNT(DISTINCT invoice) AS frequency,
    ROUND(SUM(line_total), 2) AS monetary
FROM cleaned_data
GROUP BY customer_id;


SELECT COUNT(*) AS cleaned_rows FROM cleaned_data;
SELECT COUNT(*) AS rfm_customers FROM rfm_summary;
SELECT * FROM rfm_summary ORDER BY monetary DESC LIMIT 5;




SELECT COUNT(*) AS cleaned_rows FROM cleaned_data;
SELECT COUNT(*) AS rfm_customers FROM rfm_summary;
SELECT * FROM rfm_summary ORDER BY monetary DESC LIMIT 5;