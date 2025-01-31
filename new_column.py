import streamlit as st
import pandas as pd
import numpy as np
import math

def main():
    st.title("Manipulação de Dados com Fórmulas Matemáticas")

    # Upload do arquivo
    uploaded_file = st.file_uploader("Envie um arquivo CSV ou Excel", type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]

        # Carregar arquivo no Pandas
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file)

        st.write("Visualização da Tabela:")
        st.dataframe(df)

        # Seleção de colunas disponíveis
        colunas_disponiveis = df.columns.tolist()

        # Permitir adicionar múltiplas fórmulas
        num_formulas = st.number_input("Quantas fórmulas deseja adicionar?", min_value=1, max_value=10, value=1)

        formulas = []
        for i in range(int(num_formulas)):
            st.subheader(f"Fórmula {i+1}")

            # Entrada da fórmula matemática
            formula = st.text_area(f"Digite a fórmula {i+1}:", key=f"formula_{i}")

            # Nome da nova coluna
            nome_coluna = st.text_input(f"Nome da nova coluna {i+1}:", f"Resultado_{i+1}", key=f"coluna_{i}")

            formulas.append((nome_coluna, formula))

        if st.button("Calcular e Adicionar Colunas"):
            for nome_coluna, formula in formulas:
                if nome_coluna and formula:
                    try:
                        # Criar um dicionário para armazenar as variáveis do DataFrame
                        variaveis = {col: df[col] for col in colunas_disponiveis}

                        # Adicionar funções matemáticas seguras ao ambiente
                        safe_funcs = {
                            "abs": abs,
                            "round": round,
                            "sqrt": np.sqrt,
                            "log": np.log,
                            "exp": np.exp,
                            "pow": pow,
                            "sin": np.sin,
                            "cos": np.cos,
                            "tan": np.tan,
                            "pi": math.pi,
                            "e": math.e
                        }

                        # Avaliar a expressão com segurança e arredondar para 2 casas decimais
                        df[nome_coluna] = eval(formula, {"__builtins__": {}}, {**variaveis, **safe_funcs}).round(2)

                        st.success(f"Coluna '{nome_coluna}' adicionada com sucesso!")

                    except Exception as e:
                        st.error(f"Erro ao calcular '{nome_coluna}': {e}")
            
            st.dataframe(df)

            # Opção de baixar o arquivo atualizado
            st.download_button(
                label="Baixar Arquivo Atualizado",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="arquivo_atualizado.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
