import sys
import os
import sqlite3
import re
import json
import discord

from cryptography.fernet import Fernet
from discord.ext import commands

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log import registro
from commands.functions import MTA_API, criptografar, descriptografar
from commands.guias_comandos import guias_comandos

def get_db_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sqlite', 'database.db'))

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator


def salvar_configuracoes(guild_id, server_name, user, password, ip, porta, resource_name):
    password_criptografada = criptografar(password)
    ip_criptografado = criptografar(ip)
    porta_criptografada = criptografar(porta)

    registro.info(f"Salvando configurações para guild_id={guild_id}:")
    registro.info(f"user={user}, password={password_criptografada}, ip={ip_criptografado}, porta={porta_criptografada}, resource_name={resource_name}")
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(''' 
        INSERT OR REPLACE INTO connectionSettings (guild_id, server_name, user, password, ip, porta, resource_name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (guild_id, server_name, user, password_criptografada, ip_criptografado, porta_criptografada, resource_name))

        conn.commit()  # Confirma as alterações no banco
        registro.info("Configuração salva no banco de dados com sucesso!")
    except sqlite3.Error as e:
        registro.error(f"Erro ao salvar configuração no banco: {e}")
    finally:
        conn.close()

def verificar_configuracoes(guild_id):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM connectionSettings WHERE guild_id = ?", (guild_id,))
    configuracao = cursor.fetchone()
    conn.close()

    if configuracao:

        password = descriptografar(configuracao[3])
        ip = descriptografar(configuracao[4])
        porta = descriptografar(configuracao[5])

        
        registro.info(f"Configuração para o servidor {configuracao[1]} (ID: {guild_id}): {configuracao}")
    else:
        registro.warning(f"Nenhuma configuração encontrada para o servidor {guild_id}")
    return configuracao

    
@commands.command(name="configurar")
@commands.check(is_admin) 
async def configurar(ctx, user: str = None, password: str = None, ip: str = None, porta: str = None, resource_name: str = None):


    missing_args = []

    if not user:
        missing_args.append("user")
    if not password:
        missing_args.append("password")
    if not ip:
        missing_args.append("ip")
    if not porta:
        missing_args.append("porta")
    if not resource_name:
        missing_args.append("resource_name")

    if missing_args:
        missing_args_str = ", ".join(missing_args)
        await ctx.send(f"Está faltando(s) os argumento(s): {missing_args_str}")
        return
    
    ip_pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
    if not ip_pattern.match(ip):
        await ctx.send(f"O IP '{ip}' não é válido. Por favor, forneça um IP válido no formato IPv4.")
        return

    try:
        porta_int = int(porta)
        if not (1 <= porta_int <= 65535):
            await ctx.send(f"A porta '{porta}' não é válida. A porta deve ser um número entre 1 e 65535.")
            return
    except ValueError:
        await ctx.send(f"A porta '{porta}' deve ser um número inteiro válido.")
        return

    configuracao_existente = verificar_configuracoes(ctx.guild.id)
    if configuracao_existente:
        await ctx.send(f"As configurações para o servidor '{ctx.guild.name}' ({ctx.guild.id}) já existem. Se você deseja atualizá-las, use o comando editconfig")
        return

    server_name = ctx.guild.name 
    try:
        salvar_configuracoes(ctx.guild.id, server_name, user, password, ip, porta, resource_name)
        await ctx.send(f"Configuração do servidor '{server_name}' ({ctx.guild.id}) salva com sucesso!")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao salvar as configurações: {e}")


@commands.command(name="editconfig")
@commands.check(is_admin) 
async def editconfig(ctx, user: str = None, password: str = None, ip: str = None, porta: str = None, resource_name: str = None):

    missing_args = []

    if not user:
        missing_args.append("user")
    if not password:
        missing_args.append("password")
    if not ip:
        missing_args.append("ip")
    if not porta:
        missing_args.append("porta")
    if not resource_name:
        missing_args.append("resource_name")

    if missing_args:
        missing_args_str = ", ".join(missing_args)
        await ctx.send(f"Está faltando(s) os argumento(s): {missing_args_str}")
        return

    ip_pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
    if not ip_pattern.match(ip):
        await ctx.send(f"O IP '{ip}' não é válido. Por favor, forneça um IP válido no formato IPv4.")
        return

    try:
        porta_int = int(porta)
        if not (1 <= porta_int <= 65535):
            await ctx.send(f"A porta '{porta}' não é válida. A porta deve ser um número entre 1 e 65535.")
            return
    except ValueError:
        await ctx.send(f"A porta '{porta}' deve ser um número inteiro válido.")
        return

    configuracao_existente = verificar_configuracoes(ctx.guild.id)
    if not configuracao_existente:
        await ctx.send(f"Configurações para o servidor '{ctx.guild.name}' não encontradas. Use o comando `!configurar` para salvar as configurações primeiro.")
        return

    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM connectionSettings WHERE guild_id = ?", (ctx.guild.id,))
        conn.commit()
        conn.close()

        registro.info(f"Configuração antiga removida para o servidor '{ctx.guild.name}'.")

    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao remover as configurações antigas: {e}")
        return

    server_name = ctx.guild.name 
    try:
        salvar_configuracoes(ctx.guild.id, server_name, user, password, ip, porta, resource_name)
        await ctx.send(f"Configurações do servidor '{server_name}' ({ctx.guild.id}) atualizadas com sucesso!")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao atualizar as configurações: {e}")



@commands.command(name="verconfig")
@commands.check(is_admin) 
async def verconfig(ctx):
    configuracao = verificar_configuracoes(ctx.guild.id)

    if not configuracao:
        await ctx.send(f"Não há configurações salvas para o servidor '{ctx.guild.name}' ({ctx.guild.id}).")
        return

    try:
        user = configuracao[2]
        password = descriptografar(configuracao[3])
        ip = descriptografar(configuracao[4])
        porta = descriptografar(configuracao[5])
        resource_name = configuracao[6]
    except IndexError:
        await ctx.send("Erro ao ler as configurações: formato inesperado.")
        return

    embed = discord.Embed(
        title="🔧 Configurações HTTP:",
        description=f"Configurações HTTP do servidor **MTA:SA** para comunicação com o bot, permitindo o envio e recebimento de dados via requisições HTTP. ",
        color=discord.Color.blue()
    )

    embed.add_field(name=f"👤 Usuário: {user}", value="", inline=False)
    embed.add_field(name=f"🔑 Senha: ||{password}||", value="", inline=False)
    embed.add_field(name=f"🌐 IP: {ip}", value="", inline=False)
    embed.add_field(name=f"📍 Porta: {porta}", value="", inline=False)
    embed.add_field(name=f"📦 Resource Name: {resource_name}", value="", inline=False)

    await ctx.send(embed=embed)


class ListaComandosView(discord.ui.View):
    def __init__(self, chunks):
        super().__init__(timeout=60)  # Timeout de 60 segundos para interação
        self.chunks = chunks  # Páginas de comandos divididas em "chunks"
        self.current_page = 0  # Página inicial

    async def update_message(self, interaction):
        embed = self.create_embed(self.chunks[self.current_page], self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self, chunk, page):
        embed = discord.Embed(
            title=f"Comandos Disponíveis (Página {page + 1}/{len(self.chunks)})",
            color=discord.Color.blue()
        )

        for idx, cmd in enumerate(chunk, start=page * 5 + 1):  # 5 comandos por página
            embed.add_field(
                name=f"🔹 {idx} - {cmd['nome']}",
                value=f"{cmd['descricao']}\n**Exemplo:** `{cmd['exemplo']}`",
                inline=False
            )

        return embed

    @discord.ui.button(label="⬅️ Voltar", style=discord.ButtonStyle.blurple)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)

    @discord.ui.button(label="Próximo ➡️", style=discord.ButtonStyle.green)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.chunks) - 1:
            self.current_page += 1
            await self.update_message(interaction)



@commands.command(name="comandos")
async def comandos(ctx):

    chunk_size = 5  
    total_commands = len(guias_comandos)
    chunks = [guias_comandos[i:i + chunk_size] for i in range(0, total_commands, chunk_size)]


    view = ListaComandosView(chunks)
    embed = view.create_embed(chunks[0], 0)


    await ctx.send(embed=embed, view=view)





############################ COMANDOS MTA SAN


@commands.command(name="enviar")
@commands.check(is_admin) 
async def enviar(ctx, *, mensagem: str):
    configuracao = verificar_configuracoes(ctx.guild.id)

    if not configuracao:
        await ctx.send(f"Configurações do servidor {ctx.guild.name} não salvas. Use !configurar primeiro.")
        return
    mta_api = MTA_API(ctx.guild.id)
    resposta = mta_api.enviar_mensagem(mensagem)
    await ctx.send(resposta)



class ListaModsView(discord.ui.View):
    def __init__(self, chunks):
        super().__init__(timeout=60) 
        self.chunks = chunks
        self.current_page = 0
        self.message = None

    async def update_message(self, interaction):
        embed = self.create_embed(self.chunks[self.current_page], self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self, chunk, page):
        embed = discord.Embed(
            title=f"Lista de Mods (Página {page + 1}/{len(self.chunks)})",
            color=discord.Color.blue()
        )

        for idx, module in enumerate(chunk, start=page * 20 + 1):
            status_icon = {
                "loaded": "🔴",
                "running": "🟢"
            }.get(module["status"], "🔴")

            status = f"{module['status']} {status_icon}"

            embed.add_field(
                name=f"{idx}. {module['name']} ━━━━━ {status}",
                value="",
                inline=False
            )
        return embed

    @discord.ui.button(label="⬅️ Voltar", style=discord.ButtonStyle.blurple)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)

    @discord.ui.button(label="Próximo ➡️", style=discord.ButtonStyle.green)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.chunks) - 1:
            self.current_page += 1
            await self.update_message(interaction)



@commands.command(name="verlistamods")
@commands.check(is_admin)
async def verlistamods(ctx):
    configuracao = verificar_configuracoes(ctx.guild.id)

    if not configuracao:
        await ctx.send(f"Configurações do servidor {ctx.guild.name} não salvas. Use !configurar primeiro.")
        return

    mta_api = MTA_API(ctx.guild.id)
    resposta = mta_api.listar_mods()

    json_str = resposta[0]
    data = json.loads(json_str)
    module_list = data[0]

    chunk_size = 20
    total_modules = len(module_list)
    chunks = [module_list[i:i + chunk_size] for i in range(0, total_modules, chunk_size)]


    view = ListaModsView(chunks)
    embed = view.create_embed(chunks[0], 0)

    await ctx.send(embed=embed, view=view)


@commands.command(name="startmod")
@commands.check(is_admin)
async def startmod(ctx, input_mod: str):
    configuracao = verificar_configuracoes(ctx.guild.id)

    if not configuracao:
        await ctx.send(f"Configurações do servidor {ctx.guild.name} não salvas. Use !configurar primeiro.")
        return


    mta_api = MTA_API(ctx.guild.id)
    

    resposta = mta_api.listar_mods()
    json_str = resposta[0]
    data = json.loads(json_str)
    module_list = data[0]


    if input_mod.isdigit():
        index = int(input_mod)

        if index < 1 or index > len(module_list):
            await ctx.send("Índice inválido! Por favor, escolha um número da lista de mods.")
            return
        mod_nome = module_list[index - 1]['name']  
    else:
     
        mod_nome = input_mod

        mod_names = [mod['name'] for mod in module_list]
        if mod_nome not in mod_names:
            await ctx.send(f"Mod '{mod_nome}' não encontrado na lista.")
            return


    resposta = mta_api.iniciar_mod(mod_nome)

    await ctx.send(resposta)
