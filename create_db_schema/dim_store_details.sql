---Drop column lat---
ALTER TABLE dim_store_details
	DROP COLUMN lat;
---Alter dim_store_details columns to correct data types---
ALTER TABLE dim_store_details 
	ALTER COLUMN address TYPE VARCHAR(255);
ALTER TABLE dim_store_details 
	ALTER COLUMN longitude TYPE FLOAT USING longitude::double precision;
ALTER TABLE dim_store_details 
	ALTER COLUMN locality TYPE VARCHAR(255);
ALTER TABLE dim_store_details 
	ALTER COLUMN store_code TYPE VARCHAR(12);
ALTER TABLE dim_store_details 
	ALTER COLUMN staff_numbers TYPE SMALLINT;
ALTER TABLE dim_store_details 
	ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE;
ALTER TABLE dim_store_details 
	ALTER COLUMN store_type TYPE VARCHAR(255);
ALTER TABLE dim_store_details 
	ALTER COLUMN store_type DROP NOT NULL;
ALTER TABLE dim_store_details 
	ALTER COLUMN latitude TYPE FLOAT USING latitude::double precision;
ALTER TABLE dim_store_details 
	ALTER COLUMN country_code TYPE VARCHAR(2);

--Web address--
UPDATE dim_store_details
SET locality = NULL
,country_code = NULL
,continent = NULL
WHERE store_code = 'WEB-1388012W';

---Create primary key on date_uuid---
--Delete nulls--
DELETE FROM dim_store_details
WHERE store_code is NULL;
--Check for duplicates in column date_uuid--
SELECT COUNT(*)
,store_code
FROM dim_store_details
GROUP BY store_code
HAVING count(*)>1;
--Set Primary Key--
ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);


