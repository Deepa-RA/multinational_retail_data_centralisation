---Alter dim_users columns to correct data types---
ALTER TABLE dim_users 
	ALTER COLUMN first_name TYPE VARCHAR(255);
ALTER TABLE dim_users 
	ALTER COLUMN last_name TYPE VARCHAR(255);
ALTER TABLE dim_users 
	ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE;
ALTER TABLE dim_users 
	ALTER COLUMN country_code TYPE VARCHAR(2);
ALTER TABLE dim_users 
	ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;
ALTER TABLE dim_users 
	ALTER COLUMN join_date TYPE DATE USING join_date::DATE;

---Create primary key on date_uuid---
--Delete nulls--
DELETE FROM dim_users
WHERE user_uuid is NULL;
--Check for duplicates in column date_uuid--
SELECT COUNT(*)
,user_uuid
FROM dim_users
GROUP BY user_uuid
HAVING count(*)>1
--Set Primary Key--
ALTER TABLE dim_users
ADD PRIMARY KEY (user_uuid);
