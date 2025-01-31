import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def carregar_dados():
    """Carrega o arquivo CSV ou Excel e retorna um DataFrame"""
    uploaded_file = st.file_uploader("Envie um arquivo CSV ou Excel", type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(uploaded_file, parse_dates=True)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file, parse_dates=True)

        st.write("Visualização da Tabela Original:")
        st.dataframe(df)

        return df
    return None

def visualizar_perfil_dados(df):
    """Exibe informações detalhadas sobre os dados"""
    if df is None:
        st.warning("Nenhum dado carregado ainda.")
        return None

    st.subheader("Perfil Holístico dos Dados")

    # Identificar colunas do tipo Timestamp
    colunas_data = df.select_dtypes(include=["datetime", "datetime64"]).columns.tolist()

    # Exibir resumo geral sem colunas de data
    st.write("### 📊 Resumo Geral (Sem colunas de data)")
    df_desc = df.drop(columns=colunas_data, errors="ignore").describe(include="all").T  # Remove colunas datetime
    st.dataframe(df_desc)

    # Exibir tipos de dados e contagem de valores nulos
    st.write("### 📌 Informações sobre os dados")
    info_df = pd.DataFrame({
        "Coluna": df.columns,
        "Tipo de Dado": df.dtypes.astype(str),
        "Valores Únicos": [df[col].nunique() for col in df.columns],
        "Valores Nulos (%)": [df[col].isna().mean() * 100 for col in df.columns]
    })
    st.dataframe(info_df)

    # Exibir principais valores de cada coluna
    st.write("### 🔥 Principais Valores por Coluna")
    for col in df.columns:
        st.write(f"**{col}**")
        st.write(df[col].value_counts().head(5))

    # Exibir distribuição gráfica dos dados
    st.write("### 📈 Distribuição dos Dados")
    col_escolhida = st.selectbox("Escolha uma coluna para visualizar a distribuição:", df.columns)

    if pd.api.types.is_numeric_dtype(df[col_escolhida]):
        # Gráfico para colunas numéricas
        fig, ax = plt.subplots()
        df[col_escolhida].hist(bins=20, ax=ax, edgecolor="black")
        ax.set_title(f"Distribuição de {col_escolhida}")
        ax.set_xlabel(col_escolhida)
        ax.set_ylabel("Frequência")
        st.pyplot(fig)
    else:
        # Gráfico para colunas categóricas
        fig, ax = plt.subplots()
        df[col_escolhida].value_counts().head(10).plot(kind="bar", ax=ax)
        ax.set_title(f"Valores mais frequentes em {col_escolhida}")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)

    return df

def main():
    st.title("Ferramenta Navegar - Estilo Alteryx")

    df = carregar_dados()

    if df is not None:
        visualizar_perfil_dados(df)

if __name__ == "__main__":
    main()
