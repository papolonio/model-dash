import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from utils.etl import carregar_dados
from utils.validator import validar_dataframe
from utils.visualizations import exibir_cards, grafico_faturamento

# Configuração
st.set_page_config(page_title="Dashboard CRM", layout="wide")

# =============== MENU NO TOPO ===============
selected = option_menu(
    menu_title=None,
    options=["Base de dados", "Dashboard"],
    icons=["database", "bar-chart-line"],
    orientation="horizontal"
)

# =============== BASE DE DADOS ===============
if selected == "Base de dados":
    st.title("📂 Base de dados - Upload e Validação")

    st.markdown("""
        Bem-vindo! Aqui você pode ter uma **prévia de como os seus dados podem ser visualizados em um dashboard**.

        ### 📝 Instruções:
        1. Baixe o modelo de planilha clicando no botão abaixo.
        2. Preencha com os dados da sua operação.
        3. Exporte como `.xlsx` ou salve direto e envie abaixo.
    """)

    try:
        with open("data/exemplo_crm.xlsx", "rb") as f:
            st.download_button("📥 Baixar modelo de planilha", f, file_name="modelo_crm.xlsx")
    except FileNotFoundError:
        st.warning("Arquivo de exemplo não encontrado. Adicione 'exemplo_crm.xlsx' na pasta data/.")

    st.markdown("---")

    uploaded_file = st.file_uploader("Envie sua planilha preenchida (.xlsx)", type=["xlsx"])

    if uploaded_file:
        try:
            df = carregar_dados(uploaded_file)
            valid_entries = validar_dataframe(df)

            if len(valid_entries) == 0:
                st.error("Nenhuma linha válida foi encontrada na planilha. Verifique os dados.")
            else:
                st.session_state["dados_processados"] = df.to_dict()
                st.success(f"Arquivo processado com sucesso! {len(valid_entries)} entradas válidas.")
                st.info("Acesse a aba *Dashboard* no menu superior para visualizar os gráficos.")
        except Exception as e:
            st.error(f"Erro ao processar a planilha: {str(e)}")

# =============== DASHBOARD ===============
elif selected == "Dashboard":
    st.title("📊 Dashboard")

    if "dados_processados" not in st.session_state:
        st.warning("Nenhum dado carregado. Volte para a aba 'Base de dados' e envie sua planilha.")
        st.stop()

    df = pd.DataFrame(st.session_state["dados_processados"])

    st.subheader("📋 Dados recebidos")
    st.dataframe(df)

    exibir_cards(df)
    st.markdown("---")
    grafico_faturamento(df)

    st.markdown("---")
    if st.button("🔁 Enviar outro arquivo"):
        st.session_state.clear()
        st.experimental_rerun()
