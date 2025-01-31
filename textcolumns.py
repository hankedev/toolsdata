import streamlit as st
import pandas as pd

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

def dividir_texto_para_colunas(df):
    """Interface para dividir texto em colunas"""
    if df is None:
        st.warning("Nenhum dado carregado ainda.")
        return None

    st.subheader("Configuração de Texto para Colunas")

    # Escolher a coluna de texto para dividir
    coluna_texto = st.selectbox("Escolha a coluna de texto para dividir:", df.columns)

    # Escolher o delimitador
    delimitador = st.text_input("Digite o delimitador para separação:", ",")

    # Escolher quantas colunas deseja criar (opcional)
    num_colunas = st.number_input("Número máximo de colunas a criar:", min_value=2, max_value=10, value=3)

    if st.button("Aplicar Separação"):
        df_dividido = df.copy()

        # 🔹 Converter para string antes de dividir, tratando valores NaN
        df_dividido[coluna_texto] = df_dividido[coluna_texto].astype(str).fillna("")

        # Verificar se o delimitador está presente nos dados
        if not any(df_dividido[coluna_texto].str.contains(delimitador, na=False)):
            st.warning(f"Nenhum valor encontrado contendo o delimitador '{delimitador}'.")
            return

        # Dividir a coluna baseada no delimitador
        colunas_extras = df_dividido[coluna_texto].str.split(delimitador, expand=True, n=num_colunas-1)

        # Renomear colunas geradas
        for i in range(colunas_extras.shape[1]):
            df_dividido[f"{coluna_texto}_part{i+1}"] = colunas_extras[i]

        st.success("Texto dividido com sucesso!")
        st.write("Visualização dos Dados Processados:")
        st.dataframe(df_dividido)

        # Opção para baixar o arquivo processado
        st.download_button(
            label="Baixar Arquivo Processado",
            data=df_dividido.to_csv(index=False).encode("utf-8"),
            file_name="texto_para_colunas.csv",
            mime="text/csv"
        )

        return df_dividido

    return None

def main():
    st.title("Ferramenta Texto para Colunas - Estilo Alteryx")

    df = carregar_dados()

    if df is not None:
        dividir_texto_para_colunas(df)

if __name__ == "__main__":
    main()
