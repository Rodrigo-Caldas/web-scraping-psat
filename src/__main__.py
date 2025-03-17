"""Módulo para execução de serviço."""

from datetime import datetime

from src.ons import ONS

if __name__ == "__main__":
    data_inicial = datetime(2022, 2, 2)
    ons = ONS(data_inicio=data_inicial)

    ons.executar()
