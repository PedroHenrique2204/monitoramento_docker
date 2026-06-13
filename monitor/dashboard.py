from flask import Flask, request
import json
import os

app = Flask(__name__)

@app.route("/")
def home():

    try:

        with open(
            "status.json",
            "r"
        ) as arquivo:

            dados = json.load(
                arquivo
            )
        with open(
    	     "config.json",
    	     "r"
	) as arquivo:

    	     config = json.load(
        	 arquivo
    	     )
    except:

        dados = {
            "status": "DESCONHECIDO",
            "ultima_verificacao": "-",
            "ultima_atualizacao": "-",
            "total_atualizacoes": 0,
            "health_check": "-"
        }

        config = {
    		"image": "-",
    		"container": "-"
        }

    return f"""
    <html>
    <head>
        <title>AutoDocker Monitor</title>
    </head>

    <body>

        <h1>AutoDocker Update Monitor</h1>


	<p>
	<a href="/">Dashboard</a> |
	<a href="/config">Configuração</a>
	</p>

        <hr>

	<p><b>Imagem Monitorada:</b>
	{config['image']}</p>

	<p><b>Container:</b>
	{config['container']}</p>

	<p><b>Health Check URL:</b>
	{config.get('healthcheck_url', '-')}</p>

	<hr>

        <p><b>Status:</b> {dados['status']}</p>

        <p><b>Última Verificação:</b>
        {dados['ultima_verificacao']}</p>

        <p><b>Última Atualização:</b>
        {dados['ultima_atualizacao']}</p>

        <p><b>Total de Atualizações:</b>
        {dados['total_atualizacoes']}</p>

        <p><b>Health Check:</b>
        {dados['health_check']}</p>

    </body>
    </html>
    """
@app.route("/config")
def config():

    if os.path.exists("config.json"):

    	with open(
        	"config.json",
        	"r"
    	) as arquivo:

        	dados = json.load(
            	arquivo
        	)

    else:

     	dados = {
        	"image": "",
        	"container": "",
        	"healthcheck_url": ""
    	}

    return f"""
    <html>

    <body>

        <h1>Configuração do Monitor</h1>
	<p>
	<a href="/">Dashboard</a> |
	<a href="/config">Configuração</a>
	</p>

    	 <form action="/salvar" method="post">

            <p>Imagem:</p>

            <input
                type="text"
                name="image"
                value="{dados['image']}"
                size="50"
            >

            <p>Container:</p>

            <input
                type="text"
                name="container"
                value="{dados['container']}"
                size="50"
            >

             <p>URL do Health Check:</p>

             <input
             	type="text"
             	name="healthcheck_url"
    		value="{dados.get('healthcheck_url', '')}"
    		size="50"
             >

            <br><br>

            <button type="submit">
                Salvar
            </button>

        </form>

    </body>

    </html>
    """

@app.route("/salvar", methods=["POST"])
def salvar():

    imagem = request.form["image"]

    container = request.form["container"]

    healthcheck_url = request.form["healthcheck_url"]

    config = {
        "image": imagem,
        "container": container,
        "healthcheck_url": healthcheck_url
    }

    with open(
        "config.json",
        "w"
    ) as arquivo:

        json.dump(
            config,
            arquivo,
            indent=4
        )

    return """
    <h2>Configuração salva com sucesso!</h2>

    <a href="/config">
        Voltar
    </a>
    """
app.run(
    host="0.0.0.0",
    port=8080
)
