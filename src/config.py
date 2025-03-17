"""Módulo de configurações gerais do projeto."""

from pydantic_settings import BaseSettings
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Configuracoes(BaseSettings):
    """Configurações e parâmetros do serviço."""

    url_login: str = "https://sintegre.ons.org.br/paginas/busca.aspx"
    data: dict[str, str] = {
        "username": "email_do_usuario",
        "password": "senha_do_usuario",
    }
    service: Service = Service(ChromeDriverManager().install())


config = Configuracoes()
