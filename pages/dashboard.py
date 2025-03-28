import streamlit as st
import pandas as pd
from utils.visualizations import exibir_cards, grafico_faturamento

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Dashboard CRM")

if "dados_processados" not in st.session_state:
    st.warning("Nenhum dado carregado. Volte para a página inicial e envie sua planilha.")
    st.stop()

df = pd.DataFrame(st.session_state["dados_processados"])

st.subheader("📋 Dados recebidos")
st.dataframe(df)  # Debug visual dos dados carregados

# === Cards e Gráfico ===
exibir_cards(df)
st.markdown("---")
grafico_faturamento(df)

st.markdown("---")
if st.button("🔁 Enviar outro arquivo"):
    st.session_state.clear()
    st.experimental_rerun()
