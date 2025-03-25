import streamlit as st
import pandas as pd
from utils.etl import carregar_dados
from utils.validator import validar_dataframe
import os

st.set_page_config(page_title="Prévia de Dashboard", layout="wide")

st.title("🚀 Prévia de Dashboard - CRM")
st.markdown(
    """
    Bem-vindo! Aqui você pode ter uma **prévia de como os seus dados podem ser visualizados em um dashboard**.

    ### 📝 Instruções:
    1. Baixe o modelo de planilha clicando no botão abaixo.
    2. Preencha com os dados da sua operação.
    3. Exporte como `.xlsx` ou salve direto e envie abaixo.
    """
)

# 📥 Download da planilha modelo
with open("data/exemplo_crm.xlsx", "rb") as f:
    st.download_button("📥 Baixar modelo de planilha", f, file_name="modelo_crm.xlsx")

st.markdown("---")

# 📤 Upload da planilha do cliente
uploaded_file = st.file_uploader("Envie sua planilha preenchida (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = carregar_dados(uploaded_file)
        valid_entries = validar_dataframe(df)

        if len(valid_entries) == 0:
            st.error("Nenhuma linha válida foi encontrada na planilha. Verifique os dados.")
        else:
            st.success(f"Arquivo processado com sucesso! {len(valid_entries)} entradas válidas.")
            st.session_state["dados_processados"] = df.to_dict()  # guarda dados para o dashboard

            st.markdown("### ✅ Vá para a aba *Dashboard* no menu lateral para visualizar os gráficos.")
    except Exception as e:
        st.error(f"Erro ao processar a planilha: {str(e)}")
