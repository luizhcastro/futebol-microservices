from flask import Flask, Response, request
from pymemcache.client import base
import json

VERSAO = "1.0"
INFO = {
    "descricao": "serviço que disponibiliza comentarios sobre jogos de futebol",
    "autor": "Luiz Henrique",
    "versao": VERSAO,
}

ALIVE = "sim"

BANCO_COMENTARIOS = "banco_comentarios"
PORTA_BANCO = 11211

servico = Flask("comentarios")


@servico.get("/")
def get():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")


@servico.get("/info")
def get_info():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")


@servico.get("/alive")
def is_alive():
    return Response(ALIVE, status=200, mimetype="text/plain")


@servico.post("/comentarios/<id_jogo>")
def gravar_comentarios(id_jogo):
    sucesso, novo_comentario = False, request.get_json()

    try:
        cliente = base.Client((BANCO_COMENTARIOS, PORTA_BANCO))
        comentarios_bytes = cliente.get(f"comentarios_{id_jogo}")
        comentarios = []
        if comentarios_bytes:
            comentarios = json.loads(comentarios_bytes.decode("utf-8"))

        comentarios.append(novo_comentario)
        cliente.set(f"comentarios_{id_jogo}", json.dumps(comentarios))

        cliente.close()

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro gravando comentarios: {str(e)}")

    return Response(status=201 if sucesso else 422)


@servico.get("/comentarios/<id_jogo>")
def get_comentarios(id_jogo):
    sucesso, comentarios = False, []

    try:
        cliente = base.Client((BANCO_COMENTARIOS, PORTA_BANCO))
        comentarios_bytes = cliente.get(f"comentarios_{id_jogo}")
        print(f"DEBUG SERVICE: comentarios_bytes for {id_jogo}: {comentarios_bytes}")
        comentarios = []
        if comentarios_bytes:
            comentarios = json.loads(comentarios_bytes.decode("utf-8"))
        print(
            f"DEBUG SERVICE: comentarios after json.loads for {id_jogo}: {comentarios}"
        )

        cliente.close()

        sucesso = True
    except Exception as e:
        print(f"ocorre um erro acessando comentarios: {str(e)}")

    return Response(
        json.dumps(comentarios if sucesso and comentarios else []),
        status=200 if sucesso else 500,
        mimetype="application/json",
    )


if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=5000, debug=True)
