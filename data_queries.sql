--Task 1: How many stores does the business have and in which country--
SELECT country_code
,COUNT(DISTINCT store_code) AS total_no_stores
FROM dim_store_details
WHERE country_code IS NOT NULL
GROUP BY country_code
ORDER BY total_no_stores DESC

--Task 2: Which locations currently have the most stores?--
SELECT locality
,COUNT(DISTINCT store_code) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7

--Task 3: Which months produced the largest amount of sales?--
SELECT ROUND(SUM(O.product_quantity*P.product_price)::numeric,2) as total_sales
,REPLACE(D.month,'.0','') AS month
FROM orders_table O
LEFT JOIN dim_date_times D
ON O.date_uuid = D.date_uuid
LEFT JOIN dim_products P
ON O.product_code = P.product_code
GROUP BY D.month
ORDER BY total_sales DESC
LIMIT 6

--Task 4: How many sales are coming from online?--
SELECT COUNT(product_code) AS number_of_sales
,SUM(product_quantity) AS product_quantity_count
,CASE WHEN store_code = 'WEB-1388012W' 
		THEN 'Web'
	  ELSE 'Offline' 
 END AS location
FROM orders_table
GROUP BY CASE WHEN store_code = 'WEB-1388012W' 
			THEN 'Web'
	  	ELSE 'Offline' 
 		END
		
--Task 5: What percentage of sales come through each type of store--
--Sales correct, percentage total a little different than expected result
;WITH sales_by_store
AS
(
SELECT S.store_type
,SUM(O.product_quantity*P.product_price) as total_sales
FROM orders_table O
LEFT JOIN dim_store_details S
ON O.store_code = S.store_code
LEFT JOIN dim_products P
ON O.product_code = P.product_code
GROUP BY S.store_type
)

SELECT store_type
,ROUND(total_sales::numeric,2) AS total_sales
,ROUND((total_sales*100/(SELECT SUM(total_sales) FROM sales_by_store))::numeric,2) AS "percentage_total(%)"
FROM sales_by_store
GROUP BY total_sales, store_type
ORDER BY total_sales DESC;

--Task 6: Which month in each year produced the highest cost of sales?--
SELECT ROUND(SUM(O.product_quantity*P.product_price)::numeric,2) as total_sales
,D.year
,D.month
FROM orders_table O
LEFT JOIN dim_date_times D
ON O.date_uuid = D.date_uuid
LEFT JOIN dim_products P
ON O.product_code = P.product_code
GROUP BY D.year
,D.month
ORDER BY total_sales DESC
LIMIT 10

--Task 7: What is your staff headcount?--
--Answer different to expected answer--
SELECT SUM(staff_numbers) AS total_staff_numbers
,country_code
FROM dim_store_details
WHERE country_code IS NOT NULL
GROUP BY country_code
ORDER BY total_staff_numbers DESC

--Task 8: Which German store type is selling the most?--

SELECT ROUND(SUM(O.product_quantity*P.product_price)::numeric,2) as total_sales
,S.store_type
,S.country_code
FROM orders_table O
LEFT JOIN dim_store_details S
ON O.store_code = S.store_code
LEFT JOIN dim_products P
ON O.product_code = P.product_code
WHERE country_code = 'DE'
GROUP BY S.store_type
,S.country_code
ORDER BY total_sales ASC

--Task 9:How quickly is the company making sales?
WITH TimeDifferences AS (
    SELECT 
        year,
        LEAD(TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', timestamp), 'YYYY-MM-DD HH24:MI:SS')) OVER (PARTITION BY year ORDER BY TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', timestamp), 'YYYY-MM-DD HH24:MI:SS')) - TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', timestamp), 'YYYY-MM-DD HH24:MI:SS') AS time_diff
    FROM 
        dim_date_times
),

AvgTimeDifferences AS (
    SELECT 
        year,
        AVG(time_diff) AS avg_time_diff
    FROM 
        TimeDifferences
    WHERE 
        time_diff IS NOT NULL
    GROUP BY 
        year
)

SELECT 
    year,
    JSON_BUILD_OBJECT(
        'hours', EXTRACT(HOUR FROM avg_time_diff), 
        'minutes', EXTRACT(MINUTE FROM avg_time_diff), 
        'seconds', EXTRACT(SECOND FROM avg_time_diff)
    ) AS actual_time_taken
FROM 
    AvgTimeDifferences
ORDER BY 
    avg_time_diff DESC;