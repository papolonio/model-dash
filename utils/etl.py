import pandas as pd
from config.settings import NOME_ABA_CRM, COLUNAS_ESPERADAS

def carregar_dados(file) -> pd.DataFrame:
    # Lê o arquivo .xlsx enviado
    df = pd.read_excel(file, sheet_name=NOME_ABA_CRM, engine="openpyxl")

    # Limpa nomes das colunas
    df.columns = [col.strip() for col in df.columns]

    # Verifica colunas obrigatórias
    if not all(col in df.columns for col in COLUNAS_ESPERADAS):
        raise ValueError("A planilha enviada não possui todas as colunas esperadas.")

    # Trata dados: remove espaços, substitui valores vazios, converte datas
    df = df[COLUNAS_ESPERADAS]  # Garante a ordem correta
    df = df.dropna(subset=["Nome", "Status"])  # Remove linhas inválidas mínimas

    # Converte datas
    df["Data de Chegada"] = pd.to_datetime(df["Data de Chegada"], errors="coerce")
    df["Data Fechamento"] = pd.to_datetime(df["Data Fechamento"], errors="coerce")

    return df
