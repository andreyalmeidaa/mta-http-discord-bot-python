# 🌐 Configuração do Resource `API_MTA` no MTA:SA

Este guia mostra como configurar o resource `API_MTA` para uso com autenticação HTTP no seu servidor MTA:SA.

---

## ✅ 1. Inicie o resource `API_MTA`

Certifique-se de que o resource `API_MTA` esteja iniciado no seu servidor:

```bash
start API_MTA

## 🛠️ 2. Configure o servidor para permitir requisições HTTP

```bash
<httpserver>1</httpserver>
<httpport>22005</httpport>
<httpusername>apiuser</httpusername>
<httppassword>apiuser</httppassword>
