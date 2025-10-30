# Projeto de Microsserviços de Futebol

Este projeto demonstra uma arquitetura de microsserviços para gerenciar informações de jogos de futebol, comentários e votos. Ele consiste em três microsserviços principais: `jogos`, `comentarios` e `votacao`, juntamente com um cliente baseado em linha de comando.

## Video explicativo
[Clique aqui para assistir o video](https://SEU-USUARIO-GITHUB.github.io/NOME-DO-REPOSITORIO/video.html)

## Microsserviços

Cada microsserviço é uma aplicação Flask que interage com uma instância dedicada do Memcached para armazenamento de dados.

### 1. Serviço de Jogos (Porta 5001)
Gerencia informações de jogos de futebol (jogos passados e futuros).

**Endpoints:**
*   `GET /`: Informações do serviço
*   `GET /info`: Informações do serviço
*   `GET /alive`: Verificação de saúde
*   `POST /jogos`: Cria novos jogos ou atualiza existentes (espera uma lista de objetos de jogo)
*   `GET /jogos`: Obtém todos os jogos

### 2. Serviço de Comentários (Porta 5002)
Gerencia comentários para jogos específicos.

**Endpoints:**
*   `GET /`: Informações do serviço
*   `GET /info`: Informações do serviço
*   `GET /alive`: Verificação de saúde
*   `POST /comentarios/<id_jogo>`: Adiciona um novo comentário a um jogo específico (espera um objeto de comentário)
*   `GET /comentarios/<id_jogo>`: Obtém todos os comentários para um jogo específico

### 3. Serviço de Votação (Porta 5003)
Gerencia votos sobre qual time vencerá um jogo futuro.

**Endpoints:**
*   `GET /`: Informações do serviço
*   `GET /info`: Informações do serviço
*   `GET /alive`: Verificação de saúde
*   `POST /votacao/<id_jogo>`: Adiciona um novo voto a um jogo específico (espera um objeto de voto)
*   `GET /votacao/<id_jogo>`: Obtém todos os votos para um jogo específico

## Armazenamento de Dados

Cada microsserviço usa uma instância dedicada do Memcached para persistência de dados:
*   `banco_jogos`: Para o serviço `jogos` (porta 11211)
*   `banco_comentarios`: Para o serviço `comentarios` (porta 11212)
*   `banco_votacao`: Para o serviço `votacao` (porta 11213)

## Configuração e Execução do Projeto

### Pré-requisitos
*   Docker e Docker Compose instalados.
*   Python 3 e `pip` (para executar `crawler.py` e `client.py` fora do Docker).

### 1. Construir e Executar Serviços com Docker Compose

Navegue até o diretório raiz do projeto (`futebol-microservices/`) e execute:

```bash
docker-compose up --build -d
```

Este comando irá:
*   Construir imagens Docker para os serviços `jogos`, `comentarios`, `votacao` e `web`.
*   Puxar as imagens `memcached` para os bancos de dados.
*   Iniciar todos os serviços em modo `detached`.

### 2. Popular Dados (usando Crawler)

O script `crawler.py` lê os dados iniciais dos arquivos JSON em `data/` e os envia para os respectivos microsserviços. Você deve executar este script *depois* que os contêineres Docker estiverem em execução.

Primeiro, certifique-se de ter as dependências Python instaladas em um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Em seguida, execute o crawler:

```bash
source venv/bin/activate
python3 crawler.py
```

Este script será executado indefinidamente, enviando dados a cada 10 segundos. Você pode pará-lo com `Ctrl+C` após o envio inicial dos dados.


### 3. Usando o Cliente Python

O script `client.py` fornece uma interface de linha de comando para interagir com os microsserviços. Você pode executá-lo após popular os dados:

```bash
source venv/bin/activate
python3 client.py
```

Este cliente agora oferece uma CLI interativa para você utilizar os serviços.

## Ambiente de Desenvolvimento

### Ambiente Virtual Python
É recomendado usar um ambiente virtual Python para gerenciar as dependências:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Desative o ambiente virtual quando terminar:

```bash
deactivate
```

### Modificando Serviços
Após fazer alterações em qualquer arquivo `servico.py`, você precisará reconstruir e reiniciar os contêineres Docker:

```bash
docker-compose down
docker-compose up --build -d
```

Lembre-se de executar novamente o `crawler.py` se quiser repopular os dados após um `docker-compose down`.
