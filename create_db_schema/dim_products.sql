---Remove £ from product_price---
UPDATE dim_products
SET product_price = REPLACE(product_price,'£','');

---Create new catrgorical column weight_class---
ALTER TABLE dim_products
	ADD COLUMN weight_class VARCHAR(14);

---Cast weight as float to clearly define conditions for weight class---
ALTER TABLE dim_products 
	ALTER COLUMN weight TYPE FLOAT USING weight::double precision;

---Set categories for weight class---
UPDATE dim_products
SET weight_class =
	CASE WHEN weight < 2 THEN 'Light'
		WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
		WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
		WHEN weight >= 140 THEN 'Truck_Required'
	ELSE 'N/A'
	END;
	
---Change column name from "removed" to "still_available"---
ALTER TABLE dim_products
	RENAME COLUMN removed to still_available;

---Fix typo and set all other rows to NULL---
UPDATE dim_products
SET still_available =
	CASE WHEN lower(still_available) = 'still_avaliable' THEN 'still_available'
		WHEN lower(still_available) = 'removed' THEN 'removed'
		ELSE NULL
	END

---Alter dim_products columns to correct data types---
ALTER TABLE dim_products
	ALTER COLUMN product_price TYPE FLOAT USING product_price::double precision;
ALTER TABLE dim_products
	ALTER COLUMN "EAN" TYPE VARCHAR(22);	--set to maximum length
ALTER TABLE dim_products
	ALTER COLUMN product_code TYPE VARCHAR(11); --set to maximum length
ALTER TABLE dim_products
	ALTER COLUMN date_added TYPE DATE USING date_added::DATE;
ALTER TABLE dim_products
	ALTER COLUMN uuid TYPE UUID USING uuid::UUID;
ALTER TABLE dim_products
	ALTER COLUMN still_available TYPE BOOLEAN USING CASE WHEN lower(still_available)='still_available' THEN TRUE ELSE FALSE END;

---Create primary key on date_uuid---
--Delete nulls--
DELETE FROM dim_products
WHERE product_code is NULL;
--Check for duplicates in column date_uuid--
SELECT COUNT(*)
,product_code
FROM dim_products
GROUP BY product_code
HAVING count(*)>1
--Set Primary Key--
ALTER TABLE dim_products
ADD PRIMARY KEY (product_code);