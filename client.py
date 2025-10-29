import urllib.request as requisicao
import json
from time import sleep

URL_JOGOS = "http://localhost:5001"
URL_COMENTARIOS = "http://localhost:5002"
URL_VOTACAO = "http://localhost:5003"


def acessar(url, method="GET", data=None):
    sucesso, conteudo = False, "[]"

    req = requisicao.Request(url, method=method)
    req.add_header("Content-Type", "application/json")

    try:
        if data:
            data = json.dumps(data).encode("utf-8")

        resposta = requisicao.urlopen(req, data=data)
        if resposta.code in [200, 201, 204]:
            conteudo_bytes = resposta.read()
            if conteudo_bytes:
                conteudo = conteudo_bytes.decode("utf-8")
            else:
                conteudo = "[]"

            sucesso = True
    except Exception as e:
        print(f"ocorreu um erro acessando a URL: {url} - {e}")

    return sucesso, conteudo


def jogos_alive():
    sucesso, alive = acessar(f"{URL_JOGOS}/alive")
    return sucesso and alive == "sim"


def comentarios_alive():
    sucesso, alive = acessar(f"{URL_COMENTARIOS}/alive")
    return sucesso and alive == "sim"


def votacao_alive():
    sucesso, alive = acessar(f"{URL_VOTACAO}/alive")
    return sucesso and alive == "sim"


def get_jogos():
    sucesso, jogos_raw = acessar(f"{URL_JOGOS}/jogos")
    jogos = []
    if sucesso:
        try:
            jogos = json.loads(jogos_raw)
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to decode JSON for jogos: {e}")
            sucesso = False
    return sucesso, jogos


def get_comentarios(id_jogo):
    sucesso, comentarios_raw = acessar(f"{URL_COMENTARIOS}/comentarios/{id_jogo}")
    comentarios = []
    if sucesso:
        try:
            comentarios = json.loads(comentarios_raw)
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to decode JSON for comentarios {id_jogo}: {e}")
            sucesso = False
    return sucesso, comentarios


def adicionar_comentario(id_jogo, comentario_data):
    sucesso, _ = acessar(
        f"{URL_COMENTARIOS}/comentarios/{id_jogo}", method="POST", data=comentario_data
    )
    return sucesso


def get_votacao(id_jogo):
    sucesso, votacao_raw = acessar(f"{URL_VOTACAO}/votacao/{id_jogo}")
    votacao = []
    if sucesso:
        try:
            votacao = json.loads(votacao_raw)
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to decode JSON for votacao {id_jogo}: {e}")
            sucesso = False
    return sucesso, votacao


def adicionar_voto(id_jogo, voto_data):
    sucesso, _ = acessar(
        f"{URL_VOTACAO}/votacao/{id_jogo}", method="POST", data=voto_data
    )
    return sucesso


def imprimir_jogos(jogos):
    print("\n--- Jogos Disponíveis ---")
    for jogo in jogos:
        print(
            f"  ID: {jogo['id_jogo']} | {jogo['time1']} x {jogo['time2']} ({jogo['data']})"
        )
    print("-------------------------\n")


def imprimir_comentarios(id_jogo, comentarios):
    print(f"\n--- Comentários do Jogo {id_jogo} ---")
    if comentarios:
        for comentario in comentarios:
            print(f"  - {comentario['autor']}: {comentario['comentario']}")
    else:
        print("  Nenhum comentário para este jogo.")
    print("-----------------------------\n")


def imprimir_votacao(id_jogo, votacao):
    print(f"\n--- Votação do Jogo {id_jogo} ---")
    if votacao:
        for voto in votacao:
            print(f"  - {voto['autor']}: {voto['voto']}")
    else:
        print("  Nenhum voto para este jogo.")
    print("---------------------------\n")


def menu_principal():
    print("\n--- Bem-vindo ao Futebol Microservices CLI ---")
    print("1. Listar jogos")
    print("2. Adicionar comentário")
    print("3. Adicionar voto")
    print("4. Sair")
    return input("Escolha uma opção: ")


def listar_jogos_e_detalhes():
    if not jogos_alive():
        print("Serviço de jogos indisponível.")
        return

    sucesso, jogos = get_jogos()
    if not sucesso or not jogos:
        print("Não há jogos disponíveis.")
        return

    imprimir_jogos(jogos)
    id_jogo = input("Digite o ID do jogo para ver os detalhes: ")
    if id_jogo.lower() == "v":
        return

    if comentarios_alive():
        sucesso, comentarios = get_comentarios(id_jogo)
        if sucesso:
            imprimir_comentarios(id_jogo, comentarios)
    else:
        print("Serviço de comentários indisponível.")

    if votacao_alive():
        sucesso, votacao = get_votacao(id_jogo)
        if sucesso:
            imprimir_votacao(id_jogo, votacao)
    else:
        print("Serviço de votação indisponível.")


def adicionar_novo_comentario():
    if not comentarios_alive():
        print("Serviço de comentários indisponível.")
        return

    id_jogo = input("Digite o ID do jogo: ")
    autor = input("Digite seu nome: ")
    comentario = input("Digite seu comentário: ")
    comentario_data = {"autor": autor, "comentario": comentario}

    if adicionar_comentario(id_jogo, comentario_data):
        print("Comentário adicionado com sucesso!")
    else:
        print("Falha ao adicionar comentário.")


def adicionar_novo_voto():
    if not votacao_alive():
        print("Serviço de votação indisponível.")
        return

    id_jogo = input("Digite o ID do jogo: ")
    autor = input("Digite seu nome: ")
    voto = input("Digite seu voto: ")
    voto_data = {"autor": autor, "voto": voto}

    if adicionar_voto(id_jogo, voto_data):
        print("Voto adicionado com sucesso!")
    else:
        print("Falha ao adicionar voto.")


if __name__ == "__main__":
    while True:
        escolha = menu_principal()
        if escolha == "1":
            listar_jogos_e_detalhes()
        elif escolha == "2":
            adicionar_novo_comentario()
        elif escolha == "3":
            adicionar_novo_voto()
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
        sleep(1)
