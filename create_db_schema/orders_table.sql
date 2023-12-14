---Alter orders_table columns to correct data types---
ALTER TABLE orders_table
	ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;
ALTER TABLE orders_table
	ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;	
ALTER TABLE orders_table
	ALTER COLUMN card_number TYPE VARCHAR(19); --set to maximum card number length
ALTER TABLE orders_table
	ALTER COLUMN store_code TYPE VARCHAR(12); --set to maximum store code length
ALTER TABLE orders_table
	ALTER COLUMN product_code TYPE VARCHAR(11); --set to maximum product code length
ALTER TABLE orders_table
	ALTER COLUMN product_quantity TYPE SMALLINT;

--Foreign Keys---
--card_number--
ALTER TABLE orders_table
ADD CONSTRAINT FK_card_number
FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);
--date_uuid--
ALTER TABLE orders_table
ADD CONSTRAINT FK_date_uuid
FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);
--product_code--
ALTER TABLE orders_table
ADD CONSTRAINT FK_product_code
FOREIGN KEY (product_code) REFERENCES dim_products(product_code);
--store_code--
ALTER TABLE orders_table
ADD CONSTRAINT FK_store_code
FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);
--user_uuid--
ALTER TABLE orders_table
ADD CONSTRAINT FK_user_uuid
FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);