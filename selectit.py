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

def selecionar_colunas(df):
    """Interface para seleção de colunas com checkbox"""
    if df is None:
        st.warning("Nenhum dado carregado ainda.")
        return None

    st.subheader("Seleção de Colunas")

    # Checkbox para selecionar todas as colunas de uma vez
    selecionar_todas = st.checkbox("Selecionar todas as colunas", value=True)

    # Lista de colunas disponíveis
    colunas_disponiveis = df.columns.tolist()

    # Dicionário para armazenar os checkboxes das colunas
    colunas_selecionadas = {}

    st.write("### Colunas disponíveis:")
    for coluna in colunas_disponiveis:
        colunas_selecionadas[coluna] = st.checkbox(coluna, value=selecionar_todas)

    # Gerar lista final de colunas selecionadas
    colunas_ativas = [col for col, selecionado in colunas_selecionadas.items() if selecionado]

    if not colunas_ativas:
        st.warning("Nenhuma coluna foi selecionada.")
        return None

    # Criar um novo DataFrame apenas com as colunas selecionadas
    df_filtrado = df[colunas_ativas]

    st.success("Colunas selecionadas com sucesso!")
    st.write("Visualização da Tabela Filtrada:")
    st.dataframe(df_filtrado)

    # Opção para baixar o arquivo atualizado
    st.download_button(
        label="Baixar Arquivo Filtrado",
        data=df_filtrado.to_csv(index=False).encode("utf-8"),
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )

    return df_filtrado

def main():
    st.title("Ferramenta de Seleção de Colunas - Estilo Alteryx")

    df = carregar_dados()

    if df is not None:
        selecionar_colunas(df)

if __name__ == "__main__":
    main()
