import streamlit as st
import pandas as pd
import plotly.express as px


DATA_PATH = "decompressed_data.csv"
df = pd.read_csv(DATA_PATH)

colunas_principais = [
    "ano", "expectativa_vida", "fecundidade_total", "mortalidade_1",
    "mortalidade_5", "razao_dependencia", "prob_sobrevivencia_40",
    "prob_sobrevivencia_60", "taxa_envelhecimento", "expectativa_anos_estudo"
]
df = df[colunas_principais]

st.title("📊 Indicadores Sociais do Brasil")

st.write("Alunos: Vitor Banuth, João Vitor")
st.subheader("📋 Estrutura dos Dados")
st.write("**Dimensões:**", df.shape)
st.write("**Tipos de Dados:**")
st.write(df.dtypes)

st.subheader("📄 Visualização dos Dados")
st.dataframe(df.head())

st.subheader("📈 Estatísticas Descritivas")
st.write(df.describe())

st.subheader("📈 Evolução dos Indicadores ao Longo dos Anos")

indicador = st.selectbox(
    "Selecione um indicador para visualizar:",
    colunas_principais[1:]
)

fig_line = px.line(df, x="ano", y=indicador, markers=True,
                   title=f"Evolução de {indicador} ao longo dos anos")
st.plotly_chart(fig_line, use_container_width=True)

st.subheader("🔗 Correlação entre Indicadores")
corr = df.corr(numeric_only=True)
st.dataframe(corr)

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Mapa de Correlação entre Indicadores"
)
st.plotly_chart(fig_corr, use_container_width=True)

st.subheader("📉 Relações Interessantes")

corr_ev_mort1 = corr.loc["expectativa_vida", "mortalidade_1"]
corr_ev_fec = corr.loc["expectativa_vida", "fecundidade_total"]

st.write(f"➡️ Correlação entre **Expectativa de Vida** e **Mortalidade até 1 ano**: {corr_ev_mort1:.2f}")
st.write(f"➡️ Correlação entre **Expectativa de Vida** e **Fecundidade Total**: {corr_ev_fec:.2f}")

if corr_ev_mort1 < 0:
    st.info("🔎 Correlação negativa: quanto menor a mortalidade infantil, maior a expectativa de vida.")
if corr_ev_fec < 0:
    st.info("🔎 Correlação negativa: quanto menor a fecundidade, maior a expectativa de vida.")

