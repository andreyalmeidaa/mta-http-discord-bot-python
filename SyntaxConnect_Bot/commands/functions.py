import sys
import os
import sqlite3
import requests
import json  
import base64
import hashlib
from cryptography.fernet import Fernet

from requests.auth import HTTPBasicAuth
from config import PASSWORD

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from log import registro


chave = hashlib.sha256(PASSWORD).digest()
chave_base64 = base64.urlsafe_b64encode(chave)
cipher = Fernet(chave_base64)

def criptografar(dado: str) -> str:
    return cipher.encrypt(dado.encode()).decode()

def descriptografar(dado_criptografado: str) -> str:
    return cipher.decrypt(dado_criptografado.encode()).decode()

def conectar_db():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sqlite', 'database.db'))
    return sqlite3.connect(db_path)

def carregar_configuracoes(guild_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM connectionSettings WHERE guild_id = ?", (guild_id,))
    configuracao = cursor.fetchone()
    conn.close()
    return configuracao  

class MTA_API:
    def __init__(self, guild_id):
        
        configuracao = carregar_configuracoes(guild_id)
        
        if configuracao:

            password = descriptografar(configuracao[3])
            ip = descriptografar(configuracao[4])
            porta = descriptografar(configuracao[5])

            self.base_url = f"http://{ip}:{porta}/{configuracao[6]}"
            self.auth = HTTPBasicAuth(configuracao[2], password)  
        else:
            raise ValueError("Configurações não encontradas para esta guild.")

    def _fazer_requisicao(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        registro.info(f"URL gerada: {url}")
        try:
            response = requests.get(url, params=params, auth=self.auth, timeout=5)
            return response
        except requests.exceptions.RequestException as e:
            return e

    def enviar_mensagem(self, mensagem):
        response = self._fazer_requisicao("/call/enviarMensagemChat", {"mensagem": mensagem})
        if isinstance(response, requests.Response):
            if response.status_code == 200:
                return "Mensagem enviada com sucesso!"
            return f"Erro ao enviar mensagem: {response.status_code} - {response.text}"
        else:
            return f"Erro na requisição: {response}"

    def listar_mods(self):
        response = self._fazer_requisicao("/call/listarMods")
        if isinstance(response, requests.Response):
            if response.status_code == 200:
                try:
                    return json.loads(response.text)  
                except json.JSONDecodeError:
                    return f"Resposta inválida do servidor: {response.text}"
            return f"Erro HTTP {response.status_code}: {response.text}"
        else:
            return f"Erro na requisição: {response}"
        

    def iniciar_mod(self, mod_nome):
        response = self._fazer_requisicao("/call/iniciarMod", {"modNome": mod_nome})
        if isinstance(response, requests.Response):
            if response.status_code == 200:
                try:

                    status = json.loads(response.text.strip())  
                    registro.info(f"Status retornado: {status}")
                    
                 
                    if status and isinstance(status, list):
                        status = status[0]
                        
      
                    if status == "started":
                        return f"O mod '{mod_nome}' foi iniciado com sucesso. 🟢"
                    elif status == "already_running":
                        return f"O mod '{mod_nome}' já está em execução. 🟢"
                    elif status == "error":
                        return f"Erro ao iniciar o mod '{mod_nome}'. ❌"
                    elif status == "not_found":
                        return f"O mod '{mod_nome}' não foi encontrado no servidor. 🚫"
                    else:
                        return f"Status desconhecido ao iniciar o mod '{mod_nome}': {status} ⚠️"
                except json.JSONDecodeError:
                    return f"Erro ao processar a resposta do servidor: {response.text} ⚠️"
            else:
                return f"Erro ao iniciar o mod '{mod_nome}': {response.status_code} - {response.text} ❌" 
        else:
            return f"Erro na requisição: {response} ❌"
