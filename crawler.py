import requests
import json
from time import sleep

JOGOS = "data/jogos.json"
COMENTARIOS = "data/comentarios.json"
VOTACAO = "data/votacao.json"

URL_JOGOS = "http://localhost:5001/jogos"
URL_COMENTARIOS = "http://localhost:5002/comentarios"
URL_VOTACAO = "http://localhost:5003/votacao"


def enviar_jogos():
    sucesso = False

    with open(JOGOS, "r") as arquivo:
        conteudo = json.load(arquivo)
        jogos = conteudo["jogos"]

        arquivo.close()

        resposta = requests.post(URL_JOGOS, json=jogos)
        sucesso = resposta.status_code == 201

    return sucesso


def enviar_comentarios():
    sucesso = False

    with open(COMENTARIOS, "r") as arquivo:
        conteudo = json.load(arquivo)
        comentarios = conteudo["comentarios"]

        arquivo.close()

        for comentario in comentarios:
            id_jogo = comentario["id_jogo"]
            resposta = requests.post(f"{URL_COMENTARIOS}/{id_jogo}", json=comentario)
            sucesso = resposta.status_code == 201

    return sucesso


def enviar_votacao():
    sucesso = False

    with open(VOTACAO, "r") as arquivo:
        conteudo = json.load(arquivo)
        votacao = conteudo["votacao"]

        arquivo.close()

        for voto in votacao:
            id_jogo = voto["id_jogo"]
            resposta = requests.post(f"{URL_VOTACAO}/{id_jogo}", json=voto)
            sucesso = resposta.status_code == 201

    return sucesso


if __name__ == "__main__":
    while True:
        if enviar_jogos():
            print("jogos enviados")
        else:
            print("erro enviando jogos")

        if enviar_comentarios():
            print("comentarios enviados")
        else:
            print("erro enviando comentarios")

        if enviar_votacao():
            print("votacao enviada")
        else:
            print("erro enviando votacao")

        sleep(10)
