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

def limpar_dados(df):
    """Interface para aplicar a limpeza de dados"""
    if df is None:
        st.warning("Nenhum dado carregado ainda.")
        return None

    st.subheader("Opções de Limpeza de Dados")

    # Remover valores nulos
    remover_nulos = st.checkbox("Remover linhas com valores nulos")

    # Preenchimento de valores nulos (Selecionar coluna específica)
    preencher_nulos = st.checkbox("Preencher valores nulos em uma coluna específica")
    
    coluna_escolhida = None
    valor_preenchimento = None

    if preencher_nulos:
        coluna_escolhida = st.selectbox("Escolha a coluna para preencher os valores nulos:", df.columns)

        # Apenas permitir números na entrada do preenchimento
        valor_preenchimento = st.text_input("Digite um número para preencher os valores nulos na coluna selecionada:")

        try:
            if valor_preenchimento:
                valor_preenchimento = valor_preenchimento.replace(",", "").replace(" ", "")
                valor_preenchimento = float(valor_preenchimento)  # Converte para número
        except ValueError:
            st.error("❌ O valor deve ser um número! Não são permitidos textos ou caracteres especiais.")
            return  # Interrompe a execução se o valor não for numérico

    # Remover duplicatas
    remover_duplicatas = st.checkbox("Remover linhas duplicadas")

    # Normalizar strings (converter para minúsculas e remover espaços extras)
    normalizar_strings = st.checkbox("Normalizar colunas de texto (minúsculas e sem espaços extras)")

    # Converter colunas numéricas
    converter_numeros = st.checkbox("Converter colunas numéricas para float")

    if st.button("Aplicar Limpeza"):
        df_limpo = df.copy()

        if remover_nulos:
            df_limpo.dropna(inplace=True)

        if preencher_nulos and coluna_escolhida and valor_preenchimento is not None:
            try:
                df_limpo[coluna_escolhida].fillna(valor_preenchimento, inplace=True)
                st.success(f"Valores nulos na coluna **{coluna_escolhida}** foram preenchidos com **{valor_preenchimento}**!")
            except Exception as e:
                st.error(f"Erro ao preencher valores nulos: {e}")

        if remover_duplicatas:
            df_limpo.drop_duplicates(inplace=True)

        if normalizar_strings:
            for col in df_limpo.select_dtypes(include=[object]).columns:
                df_limpo[col] = df_limpo[col].str.lower().str.strip()

        if converter_numeros:
            for col in df_limpo.columns:
                try:
                    df_limpo[col] = pd.to_numeric(df_limpo[col].str.replace(",", "").str.replace(".", ""), errors='coerce')
                except:
                    pass  # Mantém as colunas não numéricas inalteradas

        # 🔹 **Forçar conversão correta antes de exibir os dados**
        for col in df_limpo.select_dtypes(include=['float', 'int']).columns:
            df_limpo[col] = df_limpo[col].astype(float)

        st.success("Limpeza aplicada com sucesso!")
        st.write("Visualização da Tabela Após Limpeza:")
        st.dataframe(df_limpo)

        # Opção para baixar o arquivo atualizado
        st.download_button(
            label="Baixar Arquivo Limpo",
            data=df_limpo.to_csv(index=False).encode("utf-8"),
            file_name="dados_limpos.csv",
            mime="text/csv"
        )
    
        return df_limpo

    return None

def main():
    st.title("Ferramenta de Limpeza de Dados")

    df = carregar_dados()

    if df is not None:
        st.subheader("Ferramenta de Limpeza de Dados")
        limpar_dados(df)

if __name__ == "__main__":
    main()
