from source_code.database_utils import DatabaseConnector
import pandas as pd
import tabula
import requests
import boto3

'''
To connect to API when extracting store data
'''
header = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}

class DataExtractor():
    """
    Class extracts data from different data sources
    """
    def __init__(self):
        """
        Initialise the DataExtractor instance.
        """
        self.db_connector = DatabaseConnector('../db_creds.yaml')
        self.engine = self.db_connector.engine
        self.db_creds = self.db_connector.db_creds

    def read_rds_table(self, table_name):
        """
        AWS AND PANDAS DATAFRAME
        Reads data from selected table in RDS database and returns it as pandas DataFrame.

        Parameters:
        - table_name (str): Name of the table to read from.

        Returns:
        - table_data (pandas DataFrame): Data from selected table.
        """
        table_data = pd.read_sql_table(table_name, self.engine).set_index('index')
        return table_data
    
    def retrieve_pdf_data(self, pdf_link):
        """
        Retrieves pdf file from pdf link returning a pandas DataFrame.

        Parameters:
        - pdf_link (str): Link to PDF.

        Returns: 
        - pdf_data (pandas DataFrame): Data extracted from PDF.
        """
        # Read pdf into list of DataFrame
        pdf_pages = tabula.read_pdf(pdf_link, pages='all')
        #Concatenate dataframes from read pdf
        pdf_data = pd.concat(pdf_pages, ignore_index=True) 
        return pdf_data
 
    
    def list_number_of_stores(self, number_of_stores_endpoint, header):
        """
        Returns number of stores from the API endpoint.
        
        Parameters:
        - number_of_stores_endpoint (str): Endpoint URL for API.
        - header (dict): Credentials to connect to API.
        
        Returns:
        - number_of_stores (int): Number of stores in the data.
        """
        # Send a GET request to the API to retrieve number of stores
        response = requests.get(number_of_stores_endpoint, headers=header)
        if response.status_code == 200:
            data = response.json()
            df = pd.json_normalize(data) 
            number_of_stores = df.number_stores[0]
            print(f'Number of stores: {number_of_stores}')
            return number_of_stores
        else:
            print(f'Request failed with status code: {response.status_code}')
            print(f'Response Text: { response.text}')

    def retrieve_stores_data(self, store_endpoint, number_of_stores, header):
        """
        Retrieves store level from API endpoint and returns as a pandas DataFrame.

        Parameters:
        - retrieve_store_endpoint (str): Base endpoint URL for individual store data.
        - number_of_stores (int): Number of stores.
        - header (dict): Credentials to connect to API.

        Returns:
        - store_data (pandas DataFrame): Combined data for all stores.
        """
        all_store_data = []
        for store_number in range(1,number_of_stores):
            response = requests.get(f'{store_endpoint}{store_number}', headers=header)
            if response.status_code == 200:
                store_data = response.json()
                all_store_data.append(store_data)
            else:
                print(f"Request failed for store {store_number} with status code: {response.status_code}")
        store_data = pd.DataFrame(all_store_data)
        return store_data
    
    def extract_from_s3(self, s3_address):
        """
        Downloads a CSV file from an S3 bucket and returns its data as a pandas DataFrame.

        Parameters:
        - s3_address (str): S3 address in the format 's3://bucket_name/file_key'.

        Returns:
        - product_data (pandas DataFrame): Data from the CSV file.
        """

        # Remove the 's3://' prefix to retrieve bucket name and file key
        s3_address = s3_address[5:]

        # Split the remaining address into bucket name and file key
        s3_info = s3_address.split('/')

        bucket = s3_info[0]
        file = '/'.join(s3_info[1:])

        # Download the file from S3
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=file)
        data = response['Body']

        # Convert the CSV data to a Pandas DataFrame and remove duplicate index column.
        product_data = pd.read_csv(data, index_col='Unnamed: 0').reset_index(drop=True)
        return product_data
        
    def extract_from_json(self, path):
        """
        Extracts a JSON file and returns a pandas DataFrame.

        Parameters:
        - path (str): Path to the JSON file.

        Returns:
        - json_data (pandas DataFrame): Data from the JSON file.
        """
        return pd.read_json(path)
    
if __name__ == "__main__":
    pass

 