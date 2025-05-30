function pegarStatusServidor()
    return "Servidor MTA está online e funcionando!"
end


function enviarMensagemChat(mensagem)
    print(mensagem)
end
addEvent("enviarMensagemChat", true)
addEventHandler("enviarMensagemChat", resourceRoot, enviarMensagemChat)

function listarMods()
    local resources = getResources() 
    local statusResources = {}  

    for _, resource in ipairs(resources) do
        local resourceName = getResourceName(resource)  
        local resourceStatus = getResourceState(resource) 
        
        table.insert(statusResources, {
            name = resourceName,
            status = resourceStatus
        })
    end
    return toJSON(statusResources)
end

function iniciarMod(modNome)
    local resource = getResourceFromName(modNome)
    if resource then
        local estado = getResourceState(resource)
        if estado ~= "running" then
            local iniciado = startResource(resource)
            if iniciado then
                return "started"  -- Indica que o mod foi iniciado com sucesso
            else
                return "error"  -- Falha ao iniciar o mod
            end
        else
            return "already_running"  -- Mod já está em execução
        end
    else
        return "not_found"  -- Mod não encontrado
    end
end
