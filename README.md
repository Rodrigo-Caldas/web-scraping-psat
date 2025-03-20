# web-scraping-psat

![texto](https://img.shields.io/static/v1?label=Python&message=3.12&color=green&style=flat-square "linguagem")

Repositório para realizar raspagem de dados do arquivo de histórico do PSAT no ONS.

## :sparkles: O que faz?

Acessa o site do sintegre a partir das credenciais do usuário e busca todo o histórico de precipitação por satélite (PSAT) a partir de um intervalo de datas.

## :warning: Requisitos

:heavy_check_mark: Google Chrome instalado

:heavy_check_mark: Python

## :computer: Como instalar os pacotes?

Para instalação dos pacotes há dois métodos: usando o gerenciador de pacotes ``pdm`` ou ``pip``.

### :scroll: Via ``pdm``

Rode o comando:

```bash 
pdm install
```

### :pencil: Via ``pip``

Crie um ambiente com o python 3.12 a partir do comando:

```bash 
python3.12 -m venv web-scraping-ons
```

Rode o comando para ativar o ambiente:

```bash 
source web-scraping-ons/bin/activate
```

## :rocket: Como usar o serviço?

No arquivo ``src/config.py`` altere as credenciais para o email e senha do usuário.

### Exemplo

```python
class Configuracoes(BaseSettings):
    """Configurações e parâmetros do serviço."""

    url_login: str = "https://sintegre.ons.org.br/paginas/busca.aspx"
    data: dict[str, str] = {
        "username": "emaildousuario@gmail.com",
        "password": "123456",
    }
    service: Service = Service(ChromeDriverManager().install())
```

No ``src/__main__.py`` altere a variável de ``data_inicial`` e crie uma ``data_final`` para o período de coleta.

### Exemplo

```python
if __name__ == "__main__":
    data_inicial = datetime(2020, 1, 1)
    data_final = datetime(2024, 8, 9)
    ons = ONS(data_inicio=data_inicial, data_final=data_final)

    ons.executar()
```

Rode o serviço com o comando:

```bash
python -m src
```
