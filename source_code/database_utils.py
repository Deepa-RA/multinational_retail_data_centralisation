import yaml
import sqlalchemy
from sqlalchemy import create_engine, inspect

#Create class to read credentials and upload data to DB
class DatabaseConnector:

    def __init__(self,creds_file):
        self.creds_file = creds_file
        self.db_creds = self.read_db_creds()
        self.engine = self.init_db_engine()
        self.upload_engine = self.upload_engine()

    # read credentials from yaml file and return dictionary of credentials
    def read_db_creds(self):
        with open(self.creds_file, 'r') as f:
            try:
                inputfile = yaml.safe_load(f)
                return inputfile  
            except yaml.YAMLError as exc:
                print(f"File configuration error: {exc}")
       
    
    def init_db_engine(self):
        # Read the credentials from the YAML file
        creds = self.db_creds
        # Extract the credentials
        database_type = 'postgresql'
        host = creds['RDS_HOST']
        username = creds['RDS_USER']
        password = creds['RDS_PASSWORD']
        database = creds['RDS_DATABASE']
        port = creds['RDS_PORT']
        # Establish connection URL
        db_conn_url = f"{database_type}://{username}:{password}@{host}:{port}/{database}"
        # Create and return the SQLAlchemy engine
        engine = sqlalchemy.create_engine(db_conn_url)
        try:
            engine.execution_options(isolation_level='AUTOCOMMIT').connect()
            return engine
        except Exception as exc:
            print(f"Connection error: {exc}")

    def list_db_tables(self):
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def upload_engine(self):
        # Credentials
        database_type = 'postgresql'
        dbapi= 'psycopg2'
        host = 'localhost'
        username = 'postgres'
        password = 'password'
        database = 'sales_data'
        port = '5433'
        # Establish connection URL
        db_conn_url = f"{database_type}+{dbapi}://{username}:{password}@{host}:{port}/{database}"
        # Create and return the SQLAlchemy engine
        upload_engine = sqlalchemy.create_engine(db_conn_url)
        try:
            upload_engine.execution_options(isolation_level='AUTOCOMMIT').connect()
            return upload_engine
        except Exception as exc:
            print(f"Connection error: {exc}")

    def upload_to_db(self, clean_data, table_name):
        """
        Uploads a clean DataFrame to the specified table in the connected database.

        Parameters:
        - clean_dataframe (pd.DataFrame): Cleaned DataFrame to be uploaded.
        - table_name (str): Name of the database table to which data will be uploaded.

        Returns:
        - str: Result of the DataFrame upload process.
        """
        db_to_sql = clean_data.to_sql(table_name, self.upload_engine, if_exists='replace', index=False)
        return db_to_sql

if __name__ == "__main__":
    pass