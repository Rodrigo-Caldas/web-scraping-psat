"""Módulo para lidar com o site sintegre."""

import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from rich.progress import Progress, BarColumn, TextColumn

from src.config import config
from src.logit import log


class ONS:
    """Classe para navegar no site do ONS."""

    def __init__(self, data_inicio: datetime, data_final: datetime = datetime.today()):
        """
        Configurações básicas para iniciar a classe.

        Parameters
        ----------
        data_inicio : datetime
            Data de início dos dados.
        data_final : datetime, optional
            Data final dos dados, by default datetime.today()
        """
        self.data_inicio = data_inicio
        self.data_final = data_final

    @property
    def nome_produto_psat(self) -> str:
        """Nome do produto de histórico PSAT."""
        return "Historico precipitacao por satelite"

    @property
    def classe_botao_ordenar(self) -> str:
        """Classe do botão 'Ordenar por'."""
        return "select2-selection__arrow"

    @property
    def caminho_xpath_mais_recentes(self) -> str:
        """Caminho XPATH para botão 'Mais Recentes'."""
        return "/html/body/form/div[12]/div/div[3]/div/div/div/div[1]/div[2]/div/div[3]/div[2]/span[2]/span/span[2]/ul/li[2]"

    @property
    def caminho_xpath_concordo(self) -> str:
        """Caminho XPATH para botão 'Concordo'."""
        return "/html/body/form/div[12]/div/div[5]/button"
    
    @property
    def caminho_xpath_ver_mais(self) -> str:
        """Caminho XPATH para botão 'Ver mais'."""
        return "/html/body/form/div[12]/div/div[3]/div/div/div/div[1]/div[1]/div/div[4]/div[2]/a"

    @property
    def caminho_xpath_produto(self) -> str:
        """Caminho XPATH para botão de filtro 'Produto'."""
        return "//label[contains(text(), 'Histórico de Precipitação por Satélite – ONS')]"

    @staticmethod
    def descer_final_da_pagina(driver: WebDriver) -> None:
        """
        Desce até o final da página da Web, independente do seu tamanho.

        Parameters
        ----------
        driver : WebDriver
            Driver do serviço chrome.

        Raises
        ------
        erro
            Erro levantado caso ocorra.
        """
        try:
            ultima_altura = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                time.sleep(1)
                nova_altura = driver.execute_script("return document.body.scrollHeight")

                if nova_altura == ultima_altura:
                    break

                ultima_altura = nova_altura

            log.info("[bright_green]Final da página concluído!")

        except Exception as erro:
            log.error("[bright_red]Erro ao descer a página!")
            raise erro

    def executar(self) -> None:
        """
        Executa o processo de baixar todos os psats.

        Raises
        ------
        erro_login
            Erro de login levantado.
        erro_pesquisa
            Erro de pesquisa levantado.
        erro_ordenacao
            Erro de ordenação levantado.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")  # Abre o navegador maximizado

        driver = webdriver.Chrome(service=config.service, options=chrome_options)
        driver.get(config.url_login)

        log.info("Logando no sintegre..")

        try:
            driver.find_element(By.ID, "username").send_keys(config.data["username"])
            driver.find_element(By.ID, "password").send_keys(config.data["password"])
            driver.find_element(By.NAME, "login").click()
            log.info("[bright_green]Login concluído!")
        
        except Exception as erro_login:
            log.error("[bright_red]Erro no login!")
            raise erro_login

        time.sleep(3)
        driver.refresh()

        log.info(f"Pesquisando produto {self.nome_produto_psat}..")

        try:
            driver.find_element(By.ID, "tbSearch").send_keys(self.nome_produto_psat)
            driver.find_element(By.NAME, "tbDataDe").send_keys(self.data_inicio.strftime("%d/%m/%Y"))
            driver.find_element(By.NAME, "tbDataAte").send_keys(self.data_final.strftime("%d/%m/%Y"))
            driver.find_element("id", "btnSearch").click()
            log.info("[bright_green]Pesquisa concluída!")

        except Exception as erro_pesquisa:
            log.error("[bright_red]Erro na pesquisa!")
            raise erro_pesquisa

        time.sleep(2)

        log.info("Ordenando o histórico no site..")

        try:
            driver.find_element(By.CLASS_NAME, self.classe_botao_ordenar).click()
            driver.find_element(By.XPATH, self.caminho_xpath_mais_recentes).click()
            driver.find_element(By.XPATH, self.caminho_xpath_concordo).click()
            time.sleep(0.5)
            driver.find_element(By.XPATH, self.caminho_xpath_ver_mais).click()
            driver.find_element(By.XPATH, self.caminho_xpath_produto).click()

            log.info("[bright_green]Ordenação concluída!")

        except Exception as erro_ordenacao:
            log.error("Erro na ordenação!")
            raise erro_ordenacao

        log.info("Descendo até o final da página..")
        self.descer_final_da_pagina(driver=driver)

        links = driver.find_elements(By.ID, "link-botao")

        with Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TextColumn("[progress.percentage]{task.percentage:>3.0f}%")) as progress:
            task = progress.add_task("[cyan]Baixando Psats através dos links...", total=len(links))

            for link in links:
                link.click()
                progress.advance(task, 1)
                time.sleep(0.2)

        log.info("[bright_green]Psats baixados!")

        driver.quit()
