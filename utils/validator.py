from pydantic import BaseModel, validator, ValidationError
from typing import Optional, List
from datetime import date
import pandas as pd

from config.settings import STATUS_VALIDOS, TEMPERATURA_VALIDA, COLUNAS_ESPERADAS

class LeadEntry(BaseModel):
    Nome: str
    Data_de_Chegada: date
    Status: str
    Origem: str
    Temperatura: str
    Valor: Optional[float]
    Data_Fechamento: Optional[date]
    Vendedor: str

    @validator("Status")
    def status_valido(cls, v):
        if v not in STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {v}")
        return v

    @validator("Temperatura")
    def temperatura_valida(cls, v):
        if v not in TEMPERATURA_VALIDA:
            raise ValueError(f"Temperatura inválida: {v}")
        return v


def validar_dataframe(df: pd.DataFrame) -> List[LeadEntry]:
    df.columns = [col.strip() for col in df.columns]

    # Confere se todas as colunas obrigatórias existem
    if not all(col in df.columns for col in COLUNAS_ESPERADAS):
        raise ValueError("A planilha não contém todas as colunas obrigatórias.")

    # Renomeia colunas para formato Pydantic (snake_case)
    df.columns = [col.replace(" ", "_") for col in df.columns]

    registros_validos = []
    for idx, row in df.iterrows():
        try:
            registro = LeadEntry(**row.to_dict())
            registros_validos.append(registro)
        except ValidationError as e:
            print(f"[ERRO] Linha {idx + 2}: {e}")  # +2 por causa do cabeçalho

    return registros_validos
