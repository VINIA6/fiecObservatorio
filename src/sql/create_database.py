import pyodbc
import os

def create_database_and_tables():
    server = os.getenv('SQL_SERVER')
    database = os.getenv('SQL_DATABASE')
    username = os.getenv('SQL_USERNAME')
    password = os.getenv('SQL_PASSWORD')
    
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};UID={username};PWD={password}'
    
    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        
        cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{database}')
        BEGIN
            CREATE DATABASE {database}
        END
        """)
        
        conn.close()
        conn_str = f'{conn_str};DATABASE={database}'
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        script_path = os.path.join(os.path.dirname(__file__), 'create_tables.sql')
        with open(script_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        for command in sql_script.split(';'):
            if command.strip():
                cursor.execute(command)
                
        conn.commit()
        print(f"Banco de dados '{database}' e tabelas criados com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar banco de dados e tabelas: {str(e)}")
        
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_database_and_tables()