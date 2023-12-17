from dataclasses import dataclass
from typing import Dict, Any, Iterable
from pandas import DataFrame
from sqlalchemy import create_engine, inspect
import pyodbc
import urllib

@dataclass(frozen=True)
class ConnectionSettings:
    """Connection Settings."""
    server: str
    database: str
    username: str
    password: str
    driver: str
    timeout: int = 30

class AzureDbConnection:
    """
    Azure SQL database connection.
    """
    def __init__(self, conn_settings: ConnectionSettings, echo: bool = False) -> None:
        conn_params = urllib.parse.quote_plus(
            'Driver=%s;' % conn_settings.driver +
            'Server=tcp:%s.database.windows.net,1433;' % conn_settings.server +
            'Database=%s;' % conn_settings.database +
            'Uid=%s;' % conn_settings.username +
            'Pwd=%s;' % conn_settings.password +
            'Encrypt=yes;' +
            'TrustServerCertificate=no;' +
            'Connection Timeout=%s;' % conn_settings.timeout
        )
        conn_string = f'mssql+pyodbc:///?odbc_connect={conn_params}'

        self.db = create_engine(conn_string, echo=echo)

    def connect(self) -> None:
        """Estimate connection."""
        self.conn = self.db.connect()

    def get_tables(self) -> Iterable[str]:
        """Get list of tables."""
        inspector = inspect(self.db)
        return [t for t in inspector.get_table_names()]

    def dispose(self) -> None:
        """Dispose opened connections."""
        self.conn.close()
        self.db.dispose()
        
        

server = 'dmsfall2023.database.windows.net'
database = 'Project'
username = 'dbAdmin'
password = 'abc123456!'
driver= '{ODBC Driver 18 for SQL Server}'
cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:dmsfall2023.database.windows.net,1433;Database=Project;Uid=dbAdmin;Pwd=abc123456!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()
conn_settings = ConnectionSettings(
    server=server, 
    database=database, 
    username=username, 
    password=password,
    driver=driver)


db_conn = AzureDbConnection(conn_settings)
db_conn.connect()


try:
    for t in db_conn.get_tables():
        print(t)
    # Do another DB-related stuff:
    # ...
finally:
    db_conn.dispose()