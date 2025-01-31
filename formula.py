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

def aplicar_formula(df):
    """Interface para aplicar fórmulas em colunas"""
    if df is None:
        st.warning("Nenhum dado carregado ainda.")
        return None

    st.subheader("Criar ou Modificar Colunas com Expressões")

    expressoes = []

    # Adicionar múltiplas expressões
    if "expressoes" not in st.session_state:
        st.session_state.expressoes = []

    num_expressoes = st.number_input("Quantas expressões deseja adicionar?", min_value=1, max_value=10, value=1)

    for i in range(num_expressoes):
        with st.expander(f"Expressão {i+1}"):
            col1, col2 = st.columns(2)

            # Escolher entre criar nova coluna ou modificar existente
            tipo_coluna = col1.radio(f"Escolha uma opção para a Expressão {i+1}", ["Criar nova coluna", "Modificar coluna existente"], key=f"tipo_{i}")

            if tipo_coluna == "Criar nova coluna":
                nome_nova_coluna = col1.text_input(f"Nome da nova coluna:", key=f"nova_coluna_{i}")
            else:
                nome_nova_coluna = col1.selectbox("Selecione a coluna existente:", df.columns, key=f"modificar_coluna_{i}")

            # Campo para escrever a fórmula
            expressao = col2.text_area(f"Digite a expressão para {nome_nova_coluna}:", key=f"expressao_{i}")

            # Ativar/desativar expressão
            habilitar = st.checkbox(f"Habilitar Expressão {i+1}", value=True, key=f"habilitar_{i}")

            expressoes.append((nome_nova_coluna, expressao, habilitar))

    if st.button("Aplicar Fórmulas"):
        df_modificado = df.copy()

        for nome_coluna, expressao, habilitar in expressoes:
            if habilitar and expressao:
                try:
                    df_modificado[nome_coluna] = df_modificado.eval(expressao)
                except Exception as e:
                    st.error(f"Erro na expressão '{expressao}': {e}")

        st.success("Fórmulas aplicadas com sucesso!")
        st.write("Visualização dos Dados Modificados:")
        st.dataframe(df_modificado)

        # Opção para baixar o arquivo atualizado
        st.download_button(
            label="Baixar Arquivo Processado",
            data=df_modificado.to_csv(index=False).encode("utf-8"),
            file_name="dados_processados.csv",
            mime="text/csv"
        )

        return df_modificado

    return None

def main():
    st.title("Ferramenta Fórmula - Estilo Alteryx")

    df = carregar_dados()

    if df is not None:
        aplicar_formula(df)

if __name__ == "__main__":
    main()
