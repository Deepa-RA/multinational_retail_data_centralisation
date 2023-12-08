import sqlalchemy
from sqlalchemy import create_engine, inspect        
def init_db_engine(self):
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