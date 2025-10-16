import streamlit as st
import pandas as pd
import plotly.express as px

DATA_PATH = "decompressed_data.csv"
df = pd.read_csv(DATA_PATH)

colunas_principais = [
    "ano",
    "expectativa_vida",
    "fecundidade_total",
    "mortalidade_1",
    "prob_sobrevivencia_60",
    "taxa_envelhecimento",
    "expectativa_anos_estudo",
    "taxa_analfabetismo_11_a_14",
    "taxa_analfabetismo_18_mais"
]

colunas_map = {
    "ano": "Ano",
    "expectativa_vida": "Expectativa de Vida",
    "fecundidade_total": "Fecundidade Total",
    "mortalidade_1": "Mortalidade até 1 ano (Por 1000 Vivos)",
    "prob_sobrevivencia_60": "Probabilidade de Sobrevivência até 60 anos",
    "taxa_envelhecimento": "Taxa de Envelhecimento",
    "expectativa_anos_estudo": "Expectativa de Anos de Estudo",
    "taxa_analfabetismo_11_a_14": "Taxa de Analfabetismo de 11 a 14 anos",
    "taxa_analfabetismo_18_mais": "Taxa de Analfabetismo de 18+ anos",
}

df = df[colunas_principais]
df.rename(columns=colunas_map, inplace=True)

st.title("📊 Indicadores Sociais do Brasil")
st.write("Alunos: **Vitor Banuth** e **João Vitor**")

st.subheader("📄 Visualização dos Dados")
st.dataframe(df.head())

st.subheader("📈 Estatísticas Descritivas")
st.write(df.describe())


st.subheader("📈 Evolução dos Indicadores ao Longo dos Anos")

indicadores_nomes = list(colunas_map.values())[1:]

indicador = st.selectbox(
    "Selecione um indicador para visualizar:",
    indicadores_nomes
)

fig_line = px.line(
    df,
    x="Ano",
    y=indicador,
    markers=True,
    title=f"Evolução de {indicador} ao longo dos anos"
)
st.plotly_chart(fig_line, use_container_width=True)

st.subheader("🔗 Mapa de Correlação entre Indicadores")

# Calcula a correlação
corr = df.corr(numeric_only=True)

# Limita valores para -0.99 e 0.99
corr = corr.clip(lower=-0.99, upper=0.99)

# Arredonda para inteiro (tira parte fracionária)
corr = corr.round(0)

# Cria o mapa de calor maior e mais legível
fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    zmin=-0.99, zmax=0.99,
    title="Mapa de Correlação entre Indicadores Sociais",
    width=1000,
    height=800
)

fig_corr.update_traces(textfont_size=14)

st.plotly_chart(fig_corr, use_container_width=True)

st.subheader("📉 Relações Interessantes")

# Calcula correlações específicas
corr_ev_mort1 = corr.loc["Expectativa de Vida", "Mortalidade até 1 ano (Por 1000 Vivos)"]
corr_ev_fec = corr.loc["Expectativa de Vida", "Fecundidade Total"]

st.write(f"➡️ Correlação entre **Expectativa de Vida** e **Mortalidade até 1 ano**: {corr_ev_mort1:.2f}")
st.write(f"➡️ Correlação entre **Expectativa de Vida** e **Fecundidade Total**: {corr_ev_fec:.2f}")

if corr_ev_mort1 < 0:
    st.info("🔎 Correlação negativa: quanto menor a mortalidade infantil, maior a expectativa de vida.")
if corr_ev_fec < 0:
    st.info("🔎 Correlação negativa: quanto menor a fecundidade, maior a expectativa de vida.")

st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")

st.subheader(" 📄 Relatório Final")

st.write("""
**Indicadores Sociais do Brasil (1991–2010):**

- A expectativa de vida aumentou de **64,7** para **73,9 anos**, indicando melhoria nas condições de saúde e qualidade de vida.  
- A fecundidade total caiu de **2,88** para **1,89 filhos por mulher**, mostrando redução no número médio de filhos e transição demográfica.  
- A mortalidade até 1 ano diminuiu de **44,68** para **16,7 por mil nascidos**, reflexo de melhorias na saúde materno-infantil.  
- A probabilidade de sobrevivência até 60 anos cresceu de **70,9%** para **84,0%**, reforçando o aumento da longevidade.  
- A taxa de envelhecimento passou de **4,83%** para **7,36%**, resultado da combinação entre menor fecundidade e maior expectativa de vida.  
- A expectativa de anos de estudo subiu de **8,16** para **9,54 anos**, mostrando avanço na escolarização média da população.  
- As taxas de analfabetismo diminuíram em todas as faixas etárias, com destaque para a faixa de **11 a 14 anos**, que caiu de **16,08%** para **3,24%**.  

**Resumo:**  
O Brasil se tornou um país com população mais escolarizada, com menos nascimentos e mais idosos, refletindo melhorias sociais e educacionais, mas também novos desafios relacionados ao envelhecimento populacional.
""")



