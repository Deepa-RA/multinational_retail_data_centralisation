# Multinational Retail Data Centralisation

## Overview
This project focuses on centralising retail data from a multinational company into a unified database.

In this project sales data is extracted from several sources, cleaned and uploaded to a SQL database. The data is further altered to create a star-based schema and then queryed to provide insights into the data.

## File usage and information
- /source: Source code
    - database_utils.py: Methods to establish connections and upload to SQL
    - database_extractor.py: Methods to extract data from various sources
    - data_cleaning.py: Methods to clean data - inconsistencies in data, missing values 

- /raw_data_processing: These notebooks utilise the source code to extract, clean and upload the data to the SQL database. The data sources include card data, date events data, orders data, products data, store data and user data - each data source has it's own jupyter notebook that preprocceses and loads the data.

- /create_db_schema: Contains SQL scripts that alter the uploaded data to create a star-based schema.

- /data_queries.sql: Contains tasks that query the data.