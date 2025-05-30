guias_comandos = [
    {
        "nome": "!configurar <usuário> <senha> <ip> <porta> <resource>",
        "descricao": "Salva as configurações do servidor MTA:SA.",
        "exemplo": "!configurar admin 123456 127.0.0.1 22005 mta_bot"
    },
    {
        "nome": "!editconfig <usuário> <senha> <ip> <porta> <resource>",
        "descricao": "Edita as configurações salvas do servidor MTA:SA.",
        "exemplo": "!editconfig admin 123456 192.168.0.1 22005 mta_bot"
    },
    {
        "nome": "!verconfig",
        "descricao": "Exibe as configurações salvas para o servidor.",
        "exemplo": "!verconfig"
    },
    {
        "nome": "!verlistamods",
        "descricao": "Lista os mods carregados no servidor, com paginação.",
        "exemplo": "!verlistamods"
    },
    {
        "nome": "!startmod <nome ou número>",
        "descricao": "Inicia um mod pelo nome ou número exibido em !verlistamods.",
        "exemplo": "!startmod FR_Login ou !startmod 3"
    },
    {
        "nome": "!stopmod <nome ou número>",
        "descricao": "Para a execução de um mod pelo nome ou número.",
        "exemplo": "!stopmod FR_Login ou !stopmod 3"
    },
    {
        "nome": "!enviar <mensagem>",
        "descricao": "Envia uma mensagem para o servidor MTA:SA.",
        "exemplo": "!enviar Olá, jogadores!"
    },
    {
        "nome": "!comandos",
        "descricao": "Exibe esta lista de comandos disponíveis no bot.",
        "exemplo": "!comandos"
    },
    # Comandos adicionais que você solicitou:
    {
        "nome": "!kickplayer <id> <motivo>",
        "descricao": "Kicka o jogador da cidade com base no id e motivo.",
        "exemplo": "!kickplayer 1234 Desrespeito aos admins"
    },
    {
        "nome": "!ban <id> <motivo> <dias>",
        "descricao": "Bane o jogador por um número específico de dias com base no id e motivo.",
        "exemplo": "!ban 1234 Uso de cheats 7"
    },
    {
        "nome": "!setmoney <id> <quantidade>",
        "descricao": "Dá uma quantidade de dinheiro a um jogador pelo id.",
        "exemplo": "!setmoney 1234 1000"
    },
    {
        "nome": "!setacl <id/usuario> <grupo>",
        "descricao": "Adiciona um jogador a um grupo de ACL pelo id ou nome de usuário.",
        "exemplo": "!setacl 1234 admin"
    },
    {
        "nome": "!playerlist",
        "descricao": "Exibe a lista de jogadores conectados no servidor.",
        "exemplo": "!playerlist"
    },
    {
        "nome": "!infoplayer <id>",
        "descricao": "Exibe as informações detalhadas de um jogador pelo id.",
        "exemplo": "!infoplayer 1234"
    },
    # Novos comandos solicitados:
    {
        "nome": "!refresh",
        "descricao": "Atualiza a lista de recursos no servidor.",
        "exemplo": "!refresh"
    },
    {
        "nome": "!restart <mod_nome>",
        "descricao": "Reinicia um mod específico no servidor.",
        "exemplo": "!restart FR_Login"
    },
    {
        "nome": "!sethealth <id> <vida>",
        "descricao": "Define a vida de um jogador pelo id.",
        "exemplo": "!sethealth 1234 100"
    },
    {
        "nome": "!setarmor <id> <quantidade>",
        "descricao": "Dá colete a um jogador pelo id.",
        "exemplo": "!setarmor 1234 50"
    },
    {
        "nome": "!setweapon <id> <arma_id>",
        "descricao": "Dá uma arma a um jogador pelo id.",
        "exemplo": "!setweapon 1234 3"
    },
    {
        "nome": "!setwl <id>",
        "descricao": "Adiciona um jogador à whitelist.",
        "exemplo": "!setwl 1234"
    }
]
