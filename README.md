# Projeto — Atualização Automática de Containers Baseada em Novas Versões de Imagens Docker

## Descrição

Solução desenvolvida para monitorar imagens Docker publicadas no DockerHub e atualizar automaticamente containers em execução quando uma nova versão da imagem for disponibilizada.

---

## Objetivo

Monitorar periodicamente uma imagem Docker identificada pela tag `latest` e, ao detectar uma atualização, realizar automaticamente:

* Download da nova imagem;
* Interrupção do container antigo;
* Remoção do container desatualizado;
* Criação de um novo container utilizando a imagem atualizada;
* Restauração automática da aplicação.

---

## Tecnologias Utilizadas

* Docker
* Docker Hub
* Python 3
* Flask
* Docker SDK for Python
---

## Estrutura do Projeto


projeto/
│
├── app/
│   ├── app.py
│   └── Dockerfile
│
├── monitor/
│   ├── monitor.py
│   ├── ultimo_digest.txt
│   └── requirements.txt
│
└── README.md
---

## Funcionamento

O sistema executa verificações periódicas na imagem Docker hospedada no Docker Hub.

Quando uma alteração é detectada:

1. A nova imagem é baixada.
2. O container atual é interrompido.
3. O container antigo é removido.
4. Um novo container é criado utilizando a imagem atualizada.
5. A aplicação volta a ficar disponível automaticamente.

---

## Fluxo de Atualização


Docker Hub
    │
    ▼
Monitor verifica digest
    │
    ▼
Nova versão encontrada?
    │
 ┌──┴──┐
 │     │
Não   Sim
 │     │
 │     ▼
 │  docker pull
 │     ▼
 │ stop container
 │     ▼
 │ remove container
 │     ▼
 │ create container
 │     ▼
 │ aplicação atualizada
 │
 ▼
aguarda próxima verificação

---

## Como Executar

### Construir a imagem

docker build -t usuario/flask-app:latest

### Enviar para o Docker Hub

docker push usuario/flask-app:latest


### Executar o monitor

python3 monitor.py

---

## Exemplo de Atualização

1. Alterar o código da aplicação.
2. Gerar uma nova imagem Docker.
3. Publicar a imagem atualizada no Docker Hub.
4. O monitor detectará automaticamente a alteração.
5. O container será atualizado sem intervenção manual.
