# AutoDocker Update Monitor

Sistema de monitoramento e atualização automática de containers Docker baseado em imagens armazenadas no Docker Hub.

## Sobre o Projeto

O AutoDocker Update Monitor foi desenvolvido com o objetivo de automatizar o processo de atualização de aplicações containerizadas. O sistema monitora periodicamente uma imagem Docker hospedada em um repositório remoto e, ao detectar uma nova versão, realiza automaticamente a atualização do container em execução.

Além da atualização automática, o projeto oferece:

* Dashboard Web para monitoramento e configuração.
* Health Check configurável.
* Notificações via Telegram.
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
* Visualizar a imagem monitorada.
* Alterar as configurações do monitor.
* Configurar a URL do Health Check.

### Notificações Telegram

O sistema envia mensagens informando:

* Detecção de novas versões.
* Atualizações realizadas.
* Resultado do Health Check.
* Possíveis erros durante o processo.

### Logs

Todas as ações realizadas pelo monitor são registradas em arquivo de log para auditoria e acompanhamento.

---

## Arquitetura do Projeto

```text
Docker Hub
     │
     ▼
Monitor Python
     │
     ├── Verifica novas imagens
     ├── Atualiza containers
     ├── Executa Health Check
     └── Envia notificações Telegram
                │
                ▼
          Dashboard Web
```

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

A configuração é realizada através do dashboard web.

Exemplo:

```json
{
    "image": "usuario/aplicacao:latest",
    "container": "nome-container",
    "healthcheck_url": "http://IP:5000/"
}
```

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

### Construir os containers

```bash
docker compose build
```

### Iniciar os serviços

```bash
docker compose up -d
```

### Verificar containers

```bash
docker ps
```

### Visualizar logs

```bash
docker logs monitor-container
```

---

## Exemplo de Atualização

1. Alterar o código da aplicação.
2. Construir uma nova imagem:

```bash
docker build -t usuario/aplicacao:latest .
```

3. Enviar para o Docker Hub:

```bash
docker push usuario/aplicacao:latest
```

4. O monitor detectará automaticamente a nova versão e realizará a atualização.

---


