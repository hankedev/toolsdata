import streamlit as st
import pandas as pd
import numpy as np

def carregar_dados():
    """Carrega o arquivo CSV ou Excel e retorna um DataFrame"""
    uploaded_file = st.file_uploader("Envie um arquivo CSV ou Excel", type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file)

        st.write("Visualização da Tabela Original:")
        st.dataframe(df)

        return df
    return None

def aplicar_amostragem(df):
    """Interface para aplicar amostragem nos dados"""
    if df is None:
        st.warning("Nenhum dado carregado ainda.")
        return None

    st.subheader("Configuração de Amostragem")

    # Escolha o tipo de amostragem
    tipo_amostra = st.radio(
        "Selecione o tipo de amostragem:",
        ["Primeiras Linhas", "Aleatório", "Percentual"]
    )

    if tipo_amostra == "Primeiras Linhas":
        num_linhas = st.number_input("Número de linhas:", min_value=1, max_value=len(df), value=10)
        df_amostra = df.head(num_linhas)

    elif tipo_amostra == "Aleatório":
        num_linhas = st.number_input("Número de linhas (amostra aleatória):", min_value=1, max_value=len(df), value=10)
        df_amostra = df.sample(n=num_linhas, random_state=42)

    elif tipo_amostra == "Percentual":
        percentual = st.slider("Percentual de amostragem:", min_value=1, max_value=100, value=10)
        num_linhas = int(len(df) * (percentual / 100))
        df_amostra = df.sample(n=num_linhas, random_state=42)

    st.write("Amostra Gerada:")
    st.dataframe(df_amostra)

    # Opção para baixar o arquivo amostrado
    st.download_button(
        label="Baixar Amostra como CSV",
        data=df_amostra.to_csv(index=False).encode("utf-8"),
        file_name="amostra.csv",
        mime="text/csv"
    )

    return df_amostra

def main():
    st.title("Ferramenta Amostra - Estilo Alteryx")

    df = carregar_dados()

    if df is not None:
        aplicar_amostragem(df)

if __name__ == "__main__":
    main()
