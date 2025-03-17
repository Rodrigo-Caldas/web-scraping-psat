"""Módulo de utilidades."""

from typing import Tuple

from bs4 import BeautifulSoup


def parse_login_form(html: str) -> Tuple[str, dict]:
    """
    Parseia html de login para encontrar o form.

    Parameters
    ----------
    html : str
        html da página de login.

    Returns
    -------
    Tuple[str, dict]
        Tupla a ser devolvida.
        Contém a url de login e informações do form para requisição.

    Raises
    ------
    ValueError
        Erro levantado caso não tenha form no html.
    """
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form")
    if not form:
        raise ValueError("No form found in the provided HTML.")

    action_url = form.get("action")  # type: ignore

    form_data = {}
    for input_elem in form.find_all("input"):  # type: ignore
        name = input_elem.get("name")
        if name:
            # Use the provided value or default to an empty string
            form_data[name] = input_elem.get("value", "")

    return action_url, form_data
