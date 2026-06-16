# Sistema de monitoramento e atualização automática de containers Docker baseado em imagens armazenadas no Docker Hub.

## Integrantes do projeto
- Ana Clara Marques
- Pedro Henrique Remigio
- Rebeca Dantas Cabral

## Sobre o Projeto

O projeto foi desenvolvido com o objetivo de automatizar o processo de atualização de aplicações containerizadas. O sistema monitora periodicamente uma imagem Docker hospedada em um repositório remoto e, ao detectar uma nova versão, realiza automaticamente a atualização do container em execução.

Além da atualização automática, o projeto oferece:

* Dashboard Web para monitoramento e configuração.
* Health Check.
* Notificações via Telegram configuráveis pelo usuário.
* Registro de logs das operações realizadas.
* Execução totalmente containerizada com Docker Compose.

---

## Objetivo

O objetivo principal do projeto é reduzir a necessidade de intervenção manual em ambientes Docker, permitindo que aplicações sejam atualizadas automaticamente sempre que uma nova imagem for publicada.

---

## Funcionalidades

### Monitoramento de Imagens Docker

O sistema verifica periodicamente o digest da imagem configurada no Docker Hub e compara com a última versão conhecida.

### Atualização Automática

Quando uma nova versão é detectada:

1. O container atual é interrompido.
2. O container antigo é removido.
3. A nova imagem é baixada.
4. Um novo container é criado automaticamente.

### Health Check

Após a atualização, o sistema realiza uma verificação em uma URL configurada pelo usuário para garantir que a aplicação está funcionando corretamente.

### Dashboard Web

O dashboard permite:

* Visualizar o status do monitor.
* Verificar a última atualização realizada.
* Consultar o total de atualizações.
* Alterar as configurações do monitor.
* Configurar a URL do Health Check.

### Notificações Telegram

O usuário pode configurar suas próprias credenciais diretamente pelo dashboard.

O sistema envia mensagens informando:

Detecção de novas versões.
Atualizações realizadas.
Resultado do Health Check.
Falhas durante o processo.
Erros encontrados pelo monitor.

### Logs

Todas as ações realizadas pelo monitor são registradas em arquivo de log para auditoria e acompanhamento.

---

## Estrutura do Projeto

```text
.
├── app
│   ├── app.py
│   └── Dockerfile
│
├── monitor
│   ├── dashboard.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── monitor.py
│   ├── requirements.txt
│   └── config.example.json
│
├── .gitignore
└── README.md
```

---

## Tecnologias Utilizadas

* Python 3
* Docker
* Docker Compose
* Flask
* Docker SDK for Python
* Requests
* Telegram Bot API

---

## Como Funciona

### Fluxo de Atualização

1. O monitor consulta o Docker Hub.
2. Obtém o digest mais recente da imagem.
3. Compara com o digest salvo anteriormente.
4. Caso exista diferença:

   * Faz o pull da nova imagem.
   * Remove o container antigo.
   * Cria um novo container.
   * Executa o Health Check.
   * Atualiza o dashboard.
   * Envia notificação para o Telegram.

---

## Configuração

Toda a configuração é realizada através do dashboard web.

Exemplo do arquivo de configuração

    "image": "usuario/aplicacao:latest",
    "container": "nome-container",
    "healthcheck_url": "http://IP:5000",
    "telegram_enabled": true,
    "telegram_token": "TOKEN_DO_BOT",
    "telegram_chat_id": "CHAT_ID"

Importante: O arquivo config.json é criado automaticamente quando as configurações são salvas pela primeira vez no dashboard.

Configurando o Telegram

## 1. Criar um Bot

Abra o Telegram.
Procure por BotFather.
Execute o comando:
/newbot
Escolha um nome para o bot.
Escolha um username para o bot.
Copie o Token fornecido pelo BotFather.

## 2. Obter o Chat ID

Envie qualquer mensagem para o seu bot.

Acesse:

https://api.telegram.org/botSEU_TOKEN/getUpdates

Substitua SEU_TOKEN pelo token recebido do BotFather.

Localize o trecho:

{
    "chat": {
        "id": 123456789
    }
}

O valor de id será o Chat ID utilizado pelo monitor.

---

## Dashboard

Após iniciar o sistema, o dashboard estará disponível em:

```text
http://IP_DO_SERVIDOR:8080
```

Informações exibidas:

* Status do monitor.
* Imagem monitorada.
* Container monitorado.
* Última verificação.
* Última atualização.
* Total de atualizações.
* Resultado do Health Check.

---

## Execução

## 1. Clonar o projeto

git clone https://github.com/PedroHenrique2204/monitoramento_docker.git

cd monitoramento_docker/monitor

---

## 2. Iniciar o monitor

docker-compose up -d

Verificar:

docker ps

Devem aparecer os containers:

monitor-container

dashboard-container

## 3. Acompanhar logs

Monitor:

docker logs -f --tail 50 monitor-container

---

## 4. Descobrir o IP da máquina

hostname -I

Exemplo:

192.168.0.38

---

## 5. Abrir o dashboard

No navegador:

http://IP_DA_MAQUINA:8080

Exemplo:

http://192.168.0.38:8080

---

## 6. Configurar o monitor

Acesse:

http://IP_DA_MAQUINA:8080/config

Preencha:

Imagem:
Nome da imagem

Exemplo:

pedro22042004/flask-app:latest

Container:
Nome do container

Exemplo:

flask-app

Health Check URL:
http://IP_DA_MAQUINA:5000

Exemplo:

http://192.168.0.38:5000

Clique em Salvar.

---

## 7. Iniciar a aplicação monitorada

Abra outro terminal:

cd ../app

docker build -t pedro22042004/flask-app:latest .

docker run -d 
--name flask-app 
-p 5000:5000 
pedro22042004/flask-app:latest

Verificar:

docker ps

---

## 8. Verificar funcionamento

Aplicação:

http://IP_DA_MAQUINA:5000

Dashboard:

http://IP_DA_MAQUINA:8080

---

## 9. Acompanhar logs

Monitor:

docker logs --tail 50 monitor-container


## 10. Testar atualização automática

Alterar o conteúdo do arquivo:

app/app.py

Exemplo:

return "Versão 2.0"

Gerar nova imagem:

docker build -t pedro22042004/flask-app:latest .

Enviar para o Docker Hub:

docker push pedro22042004/flask-app:latest

Aguardar até 30 segundos.

O monitor irá:

* Detectar novo digest
* Baixar a nova imagem
* Remover o container antigo
* Criar o novo container
* Executar o Health Check
* Atualizar o dashboard
* Enviar notificação para o Telegram
