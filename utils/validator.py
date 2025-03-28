from pydantic import BaseModel, validator, ValidationError
from typing import Optional, List
from datetime import date
import pandas as pd
from config.settings import STATUS_VALIDOS, TEMPERATURA_VALIDA, COLUNAS_ESPERADAS

class LeadEntry(BaseModel):
    Nome: str
    Data_de_Chegada: Optional[date]
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

    if not all(col in df.columns for col in COLUNAS_ESPERADAS):
        raise ValueError("A planilha não contém todas as colunas obrigatórias.")

    df.columns = [col.replace(" ", "_") for col in df.columns]

    registros_validos = []
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        row_dict["Valor"] = float(row_dict["Valor"]) if pd.notnull(row_dict["Valor"]) else None
        row_dict["Data_de_Chegada"] = pd.to_datetime(row_dict["Data_de_Chegada"], errors="coerce").date() if pd.notnull(row_dict["Data_de_Chegada"]) else None
        row_dict["Data_Fechamento"] = pd.to_datetime(row_dict["Data_Fechamento"], errors="coerce").date() if pd.notnull(row_dict["Data_Fechamento"]) else None

        try:
            registro = LeadEntry(**row_dict)
            registros_validos.append(registro)
        except ValidationError as e:
            print(f"[ERRO] Linha {idx + 2}: {e}")

    return registros_validos
