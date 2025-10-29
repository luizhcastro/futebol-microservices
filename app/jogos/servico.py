from flask import Flask, Response, request
from pymemcache.client import base
import json

VERSAO = "1.0"
INFO = {
    "descricao": "serviço que disponibiliza informações sobre jogos de futebol",
    "autor": "Luiz Henrique",
    "versao": VERSAO,
}

ALIVE = "sim"

BANCO_JOGOS = "banco_jogos"
PORTA_BANCO = 11211

servico = Flask("jogos")


@servico.get("/")
def get():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")


@servico.get("/info")
def get_info():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")


@servico.get("/alive")
def is_alive():
    return Response(ALIVE, status=200, mimetype="text/plain")


@servico.post("/jogos")
def gravar_jogos():
    sucesso, novos_jogos = False, request.get_json()

    try:
        cliente = base.Client((BANCO_JOGOS, PORTA_BANCO))
        jogos_existentes_bytes = cliente.get("jogos")
        jogos_existentes = []
        if jogos_existentes_bytes:
            jogos_existentes = json.loads(jogos_existentes_bytes.decode("utf-8"))

        # Update existing games or add new ones
        for novo_jogo in novos_jogos:
            found = False
            for i, jogo_existente in enumerate(jogos_existentes):
                if jogo_existente["id_jogo"] == novo_jogo["id_jogo"]:
                    jogos_existentes[i] = novo_jogo
                    found = True
                    break
            if not found:
                jogos_existentes.append(novo_jogo)

        cliente.set("jogos", json.dumps(jogos_existentes))

        cliente.close()

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro gravando jogos: {str(e)}")

    return Response(status=201 if sucesso else 422)


@servico.get("/jogos")
def get_jogos():
    sucesso, jogos = False, None

    try:
        cliente = base.Client((BANCO_JOGOS, PORTA_BANCO))
        jogos_bytes = cliente.get("jogos")
        if jogos_bytes:
            jogos = json.loads(jogos_bytes.decode("utf-8"))

        cliente.close()

        sucesso = True
    except Exception as e:
        print(f"ocorre um erro acessando jogos: {str(e)}")

    return Response(
        json.dumps(jogos if sucesso and jogos else []),
        status=200 if sucesso else 500,
        mimetype="application/json",
    )


if __name__ == "__main__":
    servico.run(host="0.0.0.0", port=5000, debug=True)
