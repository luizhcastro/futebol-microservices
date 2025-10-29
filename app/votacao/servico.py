from flask import Flask, Response, request
from pymemcache.client import base
import json

VERSAO = "1.0"
INFO = {
    "descricao": "serviço que disponibiliza votacao sobre jogos de futebol",
    "autor": "Luiz Henrique",
    "versao": VERSAO,
}

ALIVE = "sim"

BANCO_VOTACAO = "banco_votacao"
PORTA_BANCO = 11211

servico = Flask("votacao")


@servico.get("/")
def get():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")


@servico.get("/info")
def get_info():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")


@servico.get("/alive")
def is_alive():
    return Response(ALIVE, status=200, mimetype="text/plain")


@servico.post("/votacao/<id_jogo>")
def gravar_votacao(id_jogo):
    sucesso, novo_voto = False, request.get_json()

    try:
        cliente = base.Client((BANCO_VOTACAO, PORTA_BANCO))
        votacao_bytes = cliente.get(f"votacao_{id_jogo}")
        votacao = []
        if votacao_bytes:
            votacao = json.loads(votacao_bytes.decode("utf-8"))

        votacao.append(novo_voto)
        cliente.set(f"votacao_{id_jogo}", json.dumps(votacao))

        cliente.close()

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro gravando votacao: {str(e)}")

    return Response(status=201 if sucesso else 422)


@servico.get("/votacao/<id_jogo>")
def get_votacao(id_jogo):
    sucesso, votacao = False, []

    try:
        cliente = base.Client((BANCO_VOTACAO, PORTA_BANCO))
        votacao_bytes = cliente.get(f"votacao_{id_jogo}")
        print(f"DEBUG SERVICE: votacao_bytes for {id_jogo}: {votacao_bytes}")
        votacao = []
        if votacao_bytes:
            votacao = json.loads(votacao_bytes.decode("utf-8"))
        print(f"DEBUG SERVICE: votacao after json.loads for {id_jogo}: {votacao}")

        cliente.close()

        sucesso = True
    except Exception as e:
        print(f"ocorre um erro acessando votacao: {str(e)}")

    return Response(
        json.dumps(votacao if sucesso and votacao else []),
        status=200 if sucesso else 500,
        mimetype="application/json",
    )


if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=5000, debug=True)
