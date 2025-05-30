import os
import sys
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from log import registro

from commands.functions import criptografar, descriptografar

def criar_tabela():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sqlite', 'database.db'))
    registro.info(f"Caminho do banco de dados (absoluto): {db_path}")

    pasta_banco = os.path.dirname(db_path)
    if not os.path.exists(pasta_banco):
        try:
            os.makedirs(pasta_banco)
            registro.info(f"Pasta '{pasta_banco}' criada com sucesso!")
        except Exception as e:
            registro.error(f"Erro ao criar a pasta '{pasta_banco}': {e}")
            return
    else:
        registro.warning(f"Pasta '{pasta_banco}' já existe.")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS connectionSettings (
            guild_id TEXT PRIMARY KEY,
            server_name TEXT NOT NULL, 
            user TEXT NOT NULL,         
            password TEXT NOT NULL,     
            ip TEXT NOT NULL,           
            porta TEXT NOT NULL,       
            resource_name TEXT NOT NULL 
        )
        ''')

        conn.commit()
        registro.info("Tabela criada com sucesso ou já existe.")
    except sqlite3.OperationalError as e:
        registro.error(f"Erro ao abrir o banco de dados: {e}")
    except Exception as e:
        registro.error(f"Erro inesperado: {e}")
    finally:
        conn.close()
