from source_code.data_extraction import DataExtractor
from source_code.database_utils import DatabaseConnector
import pandas as pd
import numpy as np
import ast

class DataCleaning():
    """
    This class contains methods to clean data from various sources.
    """

    def __init__(self):
        """
        Initialises the DataCleaning instance.
        """
        self.db_connector = DatabaseConnector('../db_creds.yaml')
        self.db_extractor = DataExtractor()

    def check_input_is_pd(self,data):
        """
        Checks if the input is a pandas DataFrame.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")  
      
    # Private Methods used for cleaning data sources. 
        
    def clean_card_numbers(self,df):
        """
        Clean card_number by removing any non numerical characters

        Parameters:
        - df (pd.DataFrame): dataframe containing card_number column to be cleaned.
        """
        df['card_number']=df['card_number'].astype('string')
        df['card_number'] = df['card_number'].str.replace('?', '')
        df['card_number'] = df['card_number'].where(df['card_number'].str.contains(r'^\d+$'), np.nan)

    def clean_continents(self, df):
        """
        Cleans continent column by removing typos and numerical values using clean_string_data.
        
        Parameters
        - df (pd.DataFrame): dataframe containing continent column to be cleaned.
        """
        df['continent'] = df['continent'].astype('string')
        df.continent = df.continent.replace('eeEurope', 'Europe')
        df.continent = df.continent.replace('eeAmerica', 'America')
        df = self.clean_string_data(df, ['continent'])
    
    def clean_country_code(self, df):
        """
        Cleans country_code column:
        - Sets length to 2
        - Sets to string type

        Parameters:
        - df (pd.DataFrame): dataframe containing country_code column to be cleaned.
        """
        df.country_code = df.country_code.replace('GGB', 'GB')
        df.loc[df.country_code.str.len() > 2, 'country_code'] = np.nan
        df.country_code = df.country_code.astype('string')
  
    def clean_dates(self, df, columns):
        """
        Cleans date data by removing incorrectly formatted data and setting format Year-Month-Day.
        
        Parameters:
        - df (pd.DataFrame): dataframe containing columns to be cleaned.
        - columns (arr): array of column names to be cleaned.
        """
        for column_name in columns:
            df[column_name] = pd.to_datetime(df[column_name], format='mixed', errors='coerce') #Convert df to datetime object
            df[column_name] = df[column_name].dt.strftime('%Y-%m-%d')#convert date to desired date format
       
    def clean_email_addresses(self, df):
        """
        Cleans email_address column by removing incorrectly formatted emails.

        Parameters:
        - df (pd.DataFrame): dataframe containing email_address column to be cleaned.
        """
        email_pattern = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
        df.loc[~df['email_address'].str.match(email_pattern), 'email_address'] = np.nan #If pattern does not match NA
        df.email_address = df.email_address.astype('string') #Convert to string
 
    def clean_expiry_dates(self, df):
        """
        Clean expiry date columns in format %m/%y e.g. 01/12

        Parameters:
        - df (pd.DataFrame): dataframe containing expiry_date column to be cleaned.
        """
        df.loc[:,'expiry_date'] = pd.to_datetime(df['expiry_date'], errors = 'coerce', format='%m/%y')

    def clean_number_data(self, df, columns):
        """
        Cleans number data by removing letters and setting to string.

        Parameters:
        - df (pd.DataFrame): dataframe containing columns to be cleaned.
        - columns (arr): array containing columns with number data to be removed of letters.
        """
        for column in columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            df[column] = df[column].astype('string')
 
    def clean_phone_numbers(self, df):
        """
        Cleans phone_number column by removing (0) and non-digit characters. 
        
        Parameters:
        - df (pd.DataFrame): dataframe containing phone_number column to be cleaned.
        """
        regex = '^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$'
        df.loc[:,'phone_number'] = df['phone_number'].str.replace('(0)', '', regex=False)
        df.loc[:,'phone_number'] = df['phone_number'].replace(r'\D+', '', regex=True)

    def clean_product_codes(self,df):
        """
        Cleans product_code to maintain code pattern of 2 digits followed by string
        
        Parameters:
        - df (pd.DataFrame): dataframe containing product_code column to be cleaned.
        """
        product_code_pattern = r'^.{2}-.*$'
        df.loc[~df['product_code'].str.match(product_code_pattern), 'product_code'] = np.nan
        df.product_code = df.product_code.astype('string')

    def clean_product_price(self, df):
        """
        Cleans product_price ensuring format £xx.xx and sets to string
        
        Parameters:
        - df (pd.DataFrame): dataframe containing product_price column to be cleaned.
        """
        df['product_price'] = df['product_price'].replace(to_replace=r'[^£.0-9]', value=np.nan, regex=True)
        df.product_price = df.product_price.astype('string')

    def clean_product_weights(self, products_data):
        """
        Converts product weights in the provided products_data DataFrame to a consistent format.
        """
        replacements = {
            'kg': '',
            'g': '/1000',
            'ml': '/1000',
            'x': '*',
            'oz': '/35.274',
            '77/1000 .': '77/1000'
        }
        products_data.loc[:, 'weight'] = products_data['weight'].replace(replacements, regex=True)
        def evaluate_expression(expression):
            try:
                result = eval(expression)
                return float(result) if '/' in expression else result
            except Exception:
                return np.nan
            
        products_data['weight'] = products_data['weight'].apply(evaluate_expression)

    def clean_staff_numbers(self, df):
        """
        Cleans staff_number by removing non-numerical values.

        Parameters:
        - df (pd.DataFrame): dataframe containing staff_number column to be cleaned.
        """
        df['staff_numbers'] = pd.to_numeric(df['staff_numbers'], errors='coerce').fillna(0).astype(int)
    
    def clean_store_codes(self, df):
        """
        Cleans store_code retaining entries that follow regex pattern only.

        Parameters:
        - df (pd.DataFrame): dataframe containing store_code column to be cleaned.
        """
        df.loc[~df['store_code'].str.match(r'^.{2,3}-.{8}$', na=False), 'store_code'] = np.nan
        df.store_code = df.store_code.astype('string')
                                   
    def clean_string_data(self, df, columns):
        """
        Cleans string data by removing numerical and NULL values and set to string.

        Parameters:
        - df (pd.DataFrame): dataframe containing columns to be cleaned.
        - columns (arr): array of column names to be cleaned.
        """
        for column_name in columns:
            df.loc[df[column_name].str.contains('\d', na=False), column_name] = np.nan
            df.loc[:, column_name] = df[column_name].replace('NULL', np.nan)
            df.loc[:, column_name] = df[column_name].astype('string')

    def clean_uuids(self, df, columns):
        """
        Removes incorrect entries with incorrect uuid format.

        Parameters:
        - df (pd.DataFrame): dataframe containing columns to be cleaned.
        - columns (arr): array of columns containing uuids to be cleaned.
        """
        for column_name in columns:    
            uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            df.loc[:,column_name] = df[column_name].astype('string')
            df.loc[~df[column_name].str.match(uuid_pattern), column_name] = np.nan
   
    # Collate to clean whole dataframes below
    def clean_card_data(self, card_data):
        """
        Cleans card_data DataFrame.
        """
        self.check_input_is_pd(card_data)
        card_data = card_data.dropna().drop_duplicates()
        self.clean_card_numbers(card_data)
        self.clean_dates(card_data, ['date_payment_confirmed'])
        self.clean_expiry_dates(card_data)

        return card_data
        
    def clean_date_events_data(self, date_events_data):
        """
        Cleans date_events_data DataFrame.
        """
        self.check_input_is_pd(date_events_data)
        date_events_data = date_events_data.dropna().drop_duplicates()
        self.clean_number_data(date_events_data, ['year','month','day'])
        date_events_data.timestamp = pd.to_datetime(date_events_data.timestamp, format='%H:%M:%S', errors='coerce').dt.time
        self.clean_uuids(date_events_data, ['date_uuid'])

        return date_events_data
    
    def clean_orders_data(self, orders_data):
        """
        Clean the provided orders_data DataFrame.
        """
        self.check_input_is_pd(orders_data)
        orders_data = orders_data.drop(columns=['level_0', 'first_name', 'last_name', '1'])
        orders_data = orders_data.drop_duplicates().dropna()
        self.clean_card_numbers(orders_data)
        self.clean_product_codes(orders_data)
        orders_data.product_quantity = pd.to_numeric(orders_data.product_quantity, errors='coerce', downcast='integer')
        self.clean_store_codes(orders_data)
        self.clean_uuids(orders_data, ['date_uuid', 'user_uuid'])
        return orders_data

    def clean_products_data(self, products_data):
        """
        Cleans the provided products_data DataFrame.
        """
        self.check_input_is_pd(products_data)
        products_data = products_data.dropna().drop_duplicates()
        self.clean_dates(products_data, ['date_added'])
        self.clean_number_data(products_data, ['EAN'])
        self.clean_product_codes(products_data)
        self.clean_product_price(products_data)
        self.clean_product_weights(products_data)
        products_data.product_name = products_data.product_name.astype('string')
        self.clean_uuids(products_data, ['uuid'])

        return products_data
    
    def clean_store_data(self, store_data):
        """
        Cleans provided store_data DataFrame.
        """
        self.check_input_is_pd(store_data)
        store_data = store_data.drop(columns=['index'])
        store_data = store_data.drop_duplicates()
        self.clean_continents(store_data)        
        self.clean_country_code(store_data)
        self.clean_dates(store_data, ['opening_date'])
        self.clean_number_data(store_data, ['longitude', 'latitude'])
        self.clean_staff_numbers(store_data)
        self.clean_store_codes(store_data)
        self.clean_string_data(store_data, ['locality'])

        return store_data
    
    def clean_user_data(self, user_data):
        """
        Cleans the provided user_data DataFrame.
        """
        self.check_input_is_pd(user_data)
        user_data = user_data.dropna().drop_duplicates()
        self.clean_country_code(user_data)
        self.clean_dates(user_data, ['join_date', 'date_of_birth']) 
        self.clean_email_addresses(user_data) 
        self.clean_phone_numbers(user_data)
        self.clean_string_data(user_data,['first_name', 'last_name', 'company','country'])
        self.clean_uuids(user_data, ['user_uuid'])
        return user_data

if __name__ == "__main__":
    pass