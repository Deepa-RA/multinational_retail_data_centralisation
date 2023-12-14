---Alter dim_date_times table columns to correct data types---
ALTER TABLE dim_date_times
	ALTER COLUMN timestamp TYPE VARCHAR(8);
ALTER TABLE dim_date_times
	ALTER COLUMN month TYPE VARCHAR(4); --set to maximum length
ALTER TABLE dim_date_times
	ALTER COLUMN year TYPE VARCHAR(6); --set to maximum product code length
ALTER TABLE dim_date_times
	ALTER COLUMN day TYPE VARCHAR(4); --set to maximum length
ALTER TABLE dim_date_times
	ALTER COLUMN time_period TYPE VARCHAR(10); --set to maximum length 
ALTER TABLE dim_date_times
	ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID; 

--Update to remove '.0' from year, month, day--
UPDATE dim_date_times
SET year = REPLACE(year,'.0','');

UPDATE dim_date_times
SET month = REPLACE(month,'.0','');

UPDATE dim_date_times
SET day = REPLACE(day,'.0','');

---Create primary key on date_uuid---
--Delete nulls--
DELETE FROM dim_date_times
WHERE date_uuid is NULL;
--Check for duplicates in column date_uuid--
SELECT COUNT(*)
,date_uuid
FROM dim_date_times
GROUP BY date_uuid
HAVING count(*)>1
--Set Primary Key--
ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);