import streamlit as st
import pandas as pd
import plotly.express as px

def exibir_cards(df: pd.DataFrame, investimento_total: float = 3000):
    total_faturamento = df[df["Status"] == "Venda"]["Valor"].sum()
    total_leads = len(df)
    vendas_realizadas = len(df[df["Status"] == "Venda"])
    vendas_perdidas = len(df[df["Status"] == "Venda Perdida"])

    custo_por_venda = investimento_total / vendas_realizadas if vendas_realizadas else 0
    custo_por_lead = investimento_total / total_leads if total_leads else 0

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("💰 Faturamento", f"R$ {total_faturamento:,.2f}")
    col2.metric("🎯 Leads", total_leads)
    col3.metric("✅ Vendas", vendas_realizadas)
    col4.metric("❌ Perdidas", vendas_perdidas)
    col5.metric("📉 Custo por Venda", f"R$ {custo_por_venda:,.2f}")
    col6.metric("👥 Custo por Lead", f"R$ {custo_por_lead:,.2f}")

def grafico_faturamento(df: pd.DataFrame):
    df_vendas = df[df["Status"] == "Venda"].copy()
    df_vendas["Data de Fechamento"] = pd.to_datetime(df_vendas["Data de Fechamento"], errors="coerce")
    df_vendas = df_vendas.dropna(subset=["Data de Fechamento"])

    vendas_por_data = df_vendas.groupby("Data de Fechamento")["Valor"].sum().reset_index()

    fig = px.bar(
        vendas_por_data,
        x="Data de Fechamento",
        y="Valor",
        title="Faturamento por Data de Fechamento",
        labels={"Valor": "Faturamento", "Data de Fechamento": "Data"},
    )

    st.plotly_chart(fig, use_container_width=True)
