import docker
import time
import requests
import json
import os

from datetime import datetime

TOKEN = "8501560136:AAHxiVB-gMjtznc66rFyczUqkA4KzAohr9E"
CHAT_ID = "5185104616"

client = docker.from_env()

CONFIG_FILE = "config.json"

def carregar_configuracao():
    if not os.path.exists(CONFIG_FILE):

        raise Exception(
            "Arquivo config.json não encontrado."
        )

    with open(
        CONFIG_FILE,
        "r"
    ) as arquivo:

        return json.load(
            arquivo
        )

def carregar_status():

    try:

        with open(
            "status.json",
            "r"
        ) as arquivo:

            return json.load(
                arquivo
            )

    except:

        return {
            "status": "ONLINE",
            "ultima_verificacao": "",
            "ultima_atualizacao": "",
            "total_atualizacoes": 0,
            "health_check": "-"
        }


def salvar_status(dados):

    with open(
        "status.json",
        "w"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4
        )

config = carregar_configuracao()

IMAGE_NAME = config["image"]
CONTAINER_NAME = config["container"]
HEALTHCHECK_URL = config.get(
    "healthcheck_url",
    "http://localhost:5000"
)
status = carregar_status()

def registrar_log(mensagem):

    horario = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    linha = f"{horario} - {mensagem}"

    print(linha)

    with open(
        "monitor.log",
        "a"
    ) as arquivo:

        arquivo.write(
            linha + "\n"
        )

def ler_configuracao():

    with open(CONFIG_FILE, "r") as arquivo:
        return json.load(arquivo)


def enviar_telegram(mensagem):

    try:

        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": mensagem
            },
            timeout=10
        )

    except Exception as erro:

        registrar_log(
            f"Erro Telegram: {erro}"
        )


def obter_digest():

    image = client.images.pull(
        IMAGE_NAME
    )

    repo_digests = image.attrs.get(
        "RepoDigests"
    )

    if repo_digests:
        return repo_digests[0]

    return None


def ler_digest_salvo():

    try:

        with open(
            "ultimo_digest.txt",
            "r"
        ) as arquivo:

            return arquivo.read().strip()

    except FileNotFoundError:

        return ""


def salvar_digest(digest):

    with open(
        "ultimo_digest.txt",
        "w"
    ) as arquivo:

        arquivo.write(digest)


def verificar_aplicacao():

    try:

        resposta = requests.get(
            HEALTHCHECK_URL,
            timeout=5
    )

        return resposta.status_code == 200

    except Exception as erro:
        registrar_log(
            f"Erro Health Chech: {erro}"
        )
        return False


print("\n========================================")
print("     AutoDocker Update Monitor")
print("========================================")
print(f"Imagem    : {IMAGE_NAME}")
print(f"Container : {CONTAINER_NAME}")
print("Intervalo : 30 segundos")
print("========================================\n")

registrar_log(
    "Monitor iniciado"
)
status["status"] = "ONLINE"

salvar_status(status)

while True:
    config = carregar_configuracao()

    IMAGE_NAME = config["image"]
    CONTAINER_NAME = config["container"]

    config = ler_configuracao()

    IMAGE_NAME = config["image"]
    CONTAINER_NAME = config["container"]

    registrar_log(
        "Verificando atualizações..."
    )
    status["ultima_verificacao"] = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
    )

    salvar_status(status)    

    if verificar_aplicacao():

    	status["health_check"] = "OK"

    else:

    	status["health_check"] = "FALHOU"

    salvar_status(status)


    try:

        digest_atual = obter_digest()

        digest_salvo = ler_digest_salvo()

        registrar_log(
            f"Digest atual: {digest_atual}"
        )

        registrar_log(
            f"Digest salvo: {digest_salvo}"
        )

        if digest_atual != digest_salvo:

            registrar_log(
                "Nova versão detectada!"
            )
            enviar_telegram(
              f"📦 Nova versão detectada\n\nImagem: {IMAGE_NAME}"
            )
          
            try:

                container = client.containers.get(
                    CONTAINER_NAME
                )

                registrar_log(
                    "Parando container antigo..."
                )

                container.stop()

                registrar_log(
                    "Removendo container antigo..."
                )

                container.remove()

                time.sleep(2)

            except Exception:

                registrar_log(
                    "Container não encontrado."
                )

            registrar_log(
                "Criando novo container..."
            )

            client.containers.run(
                IMAGE_NAME,
                name=CONTAINER_NAME,
                ports={"5000/tcp": 5000},
                detach=True
            )

            registrar_log(
                "Aguardando inicialização da aplicação..."
            )

            time.sleep(5)

            if verificar_aplicacao():

                salvar_digest(
                    digest_atual
                )

                registrar_log(
                    "Health Check OK - aplicação funcionando."
                )
                status["health_check"] = "OK"

                status["total_atualizacoes"] += 1
                status["ultima_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                salvar_status(status)

                registrar_log(
                    "Container atualizado com sucesso!"
                )
                enviar_telegram(
                    f"✅ Atualização concluída\n\nImagem: {IMAGE_NAME}\nContainer: {CONTAINER_NAME}"
                )
            else:

                registrar_log(
                    "Health Check FALHOU!"
                )
                enviar_telegram(
                    f"❌ Health Check falhou\n\nImagem: {IMAGE_NAME}"
                )
                status["health_check"] = "FALHOU"

                salvar_status(status)                

                registrar_log(
                    "Aplicação não respondeu corretamente."
                )

        else:

            registrar_log(
                "Nenhuma atualização encontrada."
            )

    except Exception as erro:

        registrar_log(
            f"ERRO: {erro}"
        )

    time.sleep(30)
