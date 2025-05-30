import logging
import os

# Caminho da pasta de logs
caminho_logs = os.path.join(os.path.dirname(__file__), 'log')
os.makedirs(caminho_logs, exist_ok=True)

# Caminho do arquivo onde os logs serão salvos
arquivo_log = os.path.join(caminho_logs, 'bot_logs.log')

# Criação do logger
registro = logging.getLogger("bot")
registro.setLevel(logging.INFO)

# Evita duplicação de handlers
if not registro.handlers:
    # Log no arquivo
    para_arquivo = logging.FileHandler(arquivo_log, encoding='utf-8')
    para_arquivo.setLevel(logging.INFO)

    # Formato do log
    formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    para_arquivo.setFormatter(formato)

    registro.addHandler(para_arquivo)

    # (Opcional) Mostrar também no terminal
    para_terminal = logging.StreamHandler()
    para_terminal.setFormatter(formato)
    registro.addHandler(para_terminal)
