import sys
import os
import discord

from discord.ext import commands
from discord import app_commands


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log import registro
from config import DISCORD_TOKEN, PREFIXO_COMANDOS, INTENTS
from commands.comandos import enviar, configurar, editconfig, verconfig, verlistamods, startmod,  comandos
from sqlite.criardb import criar_tabela  

criar_tabela()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

comandos = [enviar, configurar, editconfig, verconfig, verlistamods, startmod, comandos]

for comando in comandos:
    bot.add_command(comando)

@bot.event
async def on_ready():
    registro.info("Bot online!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"O comando que você tentou executar não existe. Use `!comandos` para ver os comandos disponíveis.")
    else:
        # Em caso de outros erros, você pode também personalizar a resposta
        await ctx.send(f"Ocorreu um erro: {str(error)}")

bot.run(DISCORD_TOKEN)



#authserial <NomedaConta> httppass ---- 

#@4NDREY Verifica se o login está com acesso Admin no servidor
#Tente também utilizar o authserial 

#authserial <NomedaConta> httppass
#Dai ele vai te retornar uma senha numerica, que seja por exemplo 1234 

#Sua senha atual é api@2025, vai ficar api@20251234 , é isso que você deve passar como senha


#addaccount apiuser api@2025

#authserial apiuser



#authserial <nome_da_conta>
#Para visualizar séries autorizadas para uma conta:

#lista authserial <nome_da_conta>
#Para remover o número de série autorizado mais recente de uma conta:

#authserial <nome_da_conta> remover
#Para habilitar o login HTTP de um IP não autorizado, use o seguinte comando para obter um código de 7 dígitos que deve ser anexado à senha de login HTTP (requer a versão do servidor 1.5.4-9.11302)

#authserial <nome_da_conta> httppass