# 🌐 Integração bot discord com MTA:SA

Este guia mostra como configurar o bot do dsicord para uso com autenticação HTTP no seu servidor MTA:SA.

---

## ✅ 1. Inicie o resource `API_MTA`

Certifique-se de que o resource `API_MTA` esteja iniciado no seu servidor:

```bash
start API_MTA
```

## 🛠️ 2. Configure o servidor para permitir requisições HTTP

Abra o arquivo mtaserver.conf localizado na raiz do seu servidor e adicione (ou edite) as seguintes linhas:

```xml
<httpserver>1</httpserver>
<httpport>22005</httpport>
<httpusername>apiuser</httpusername>
<httppassword>apiuser</httppassword>
```
## 🔐 3. Criar a conta HTTP no console do servidor

```bash
addaccount apiuser api@2025
authserial apiuser httppass
```
Esse comando vai retornar algo como:
```bash
Ex: Senha de acesso: 1234567
```
Sua senha final de autenticação será:


```bash
Ex: api@20251234567
```

## ❄️ 4. Criar grupo ACL para a API

Adicione o seguinte grupo no arquivo acl.xml:

## 🔓 5. Criar a ACL webapi_access

No mesmo arquivo acl.xml, adicione as permissões necessárias:

```xml
<acl name="webapi_access">
    <right name="function.listarMods" access="true" />
    <right name="function.enviarMensagemChat" access="true" />
    <right name="function.iniciarMod" access="true" />
    <!-- Adicione outras funções exportadas pelo seu resource conforme necessário -->
</acl>
```

## 🔧 6. Dar permissões administrativas (opcional)

Se você quiser que apiuser também tenha permissões administrativas no servidor para o resource API_MTA, adicione as seguintes linhas na ACL admin (ou equivalente):

```xml
<object name="user.apiuser" />
<object name="resource.API_MTA" />
```

## ♻️ 7. Reinicie o servido

---

## 🤖 8. Configurar o bot no Discord

Depois de criar um bot no Discord, definir um **token** e adicionar ele ao seu servidor com permissões de administrador, você pode usar o seguinte comando no chat do Discord para configurar a conexão com a API do seu servidor MTA:

```plaintext
!configurar <usuário_http> <senha_http> <ip_servidor> <porta_http> <nome_do_resource>
```
Exemplo:

```plaintext
!configurar apiuser api@2025 127.0.0.1 22005 API_MTA
```

## 💾 9. O que acontece ao usar o comando?

As informações fornecidas serão salvas automaticamente no banco de dados SQLite do bot.

Você pode adicionar o mesmo bot em vários servidores do Discord.

É possível configurar múltiplas conexões HTTP (para diferentes servidores MTA) porque o bot suporta múltiplas guilds (servidores Discord).
