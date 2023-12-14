---Alter dim_card_details table columns to correct data types---
ALTER TABLE dim_card_details
	ALTER COLUMN card_number TYPE VARCHAR(19);
ALTER TABLE dim_card_details 
	ALTER COLUMN expiry_date TYPE VARCHAR(19);
ALTER TABLE dim_card_details 
	ALTER COLUMN card_provider TYPE VARCHAR(27);
ALTER TABLE dim_card_details 
	ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;
	
---Create primary key on card number---
--Delete nulls--
DELETE FROM dim_card_details
WHERE card_number is NULL;
--Check for duplicates in card_numbers--
SELECT COUNT(*)
,card_number
FROM dim_card_details
GROUP BY card_number
HAVING count(*)>1
--Set Primary Key--
ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);
