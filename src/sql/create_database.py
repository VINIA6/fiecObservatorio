import pyodbc
import sqlalchemy

server = "mssql"       # nome do serviço Docker
database = "ANTAQ"
username = "SA"
password = "ViniA63068"

connection_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
)

engine = sqlalchemy.create_engine(f"mssql+pyodbc:///?odbc_connect={connection_str}")
