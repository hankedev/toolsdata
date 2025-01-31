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

def filtrar_dados(df):
    """Interface para aplicar filtros nos dados"""
    if df is None:
        st.warning("Nenhum dado carregado ainda.")
        return None, None

    st.subheader("Configuração do Filtro")

    # Escolha entre "Filtro Básico" ou "Filtro Personalizado"
    tipo_filtro = st.radio("Selecione o tipo de filtro:", ["Filtro Básico", "Filtro Personalizado"])

    # Selecione a coluna para aplicar o filtro
    coluna_escolhida = st.selectbox("Escolha a coluna para filtrar:", df.columns)

    df_filtrado_verdadeiro = df
    df_filtrado_falso = df

    if tipo_filtro == "Filtro Básico":
        operadores_numericos = ["=", "!=", ">", ">=", "<", "<="]
        operadores_texto = ["=", "!=", "contains", "not contains", "is null", "is not null"]
        
        # Determinar se a coluna é numérica ou texto
        if pd.api.types.is_numeric_dtype(df[coluna_escolhida]):
            operadores = operadores_numericos
        else:
            operadores = operadores_texto

        operador = st.selectbox("Escolha um operador:", operadores)
        valor = st.text_input("Digite o valor para filtrar:")

        if st.button("Aplicar Filtro"):
            try:
                if operador == "=":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida] == valor]
                elif operador == "!=":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida] != valor]
                elif operador == ">":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida].astype(float) > float(valor)]
                elif operador == ">=":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida].astype(float) >= float(valor)]
                elif operador == "<":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida].astype(float) < float(valor)]
                elif operador == "<=":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida].astype(float) <= float(valor)]
                elif operador == "contains":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida].astype(str).str.contains(valor, case=False, na=False)]
                elif operador == "not contains":
                    df_filtrado_verdadeiro = df[~df[coluna_escolhida].astype(str).str.contains(valor, case=False, na=False)]
                elif operador == "is null":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida].isna()]
                elif operador == "is not null":
                    df_filtrado_verdadeiro = df[df[coluna_escolhida].notna()]
                
                df_filtrado_falso = df.drop(df_filtrado_verdadeiro.index)
                
                st.success("Filtro aplicado com sucesso!")

            except Exception as e:
                st.error(f"Erro ao aplicar o filtro: {e}")

    elif tipo_filtro == "Filtro Personalizado":
        condicao = st.text_area("Digite a condição do filtro (ex: `Age > 30 and Region == 'South'`)")

        if st.button("Aplicar Filtro Personalizado"):
            try:
                df_filtrado_verdadeiro = df.query(condicao)
                df_filtrado_falso = df.drop(df_filtrado_verdadeiro.index)

                st.success("Filtro personalizado aplicado com sucesso!")

            except Exception as e:
                st.error(f"Erro ao aplicar filtro personalizado: {e}")

    # Exibir os resultados filtrados
    st.write("### Saída - Verdadeiro (T)")
    st.dataframe(df_filtrado_verdadeiro)

    st.write("### Saída - Falso (F)")
    st.dataframe(df_filtrado_falso)

    # Opção para baixar os arquivos filtrados
    st.download_button(
        label="Baixar T (Verdadeiro)",
        data=df_filtrado_verdadeiro.to_csv(index=False).encode("utf-8"),
        file_name="dados_filtrados_verdadeiro.csv",
        mime="text/csv"
    )

    st.download_button(
        label="Baixar F (Falso)",
        data=df_filtrado_falso.to_csv(index=False).encode("utf-8"),
        file_name="dados_filtrados_falso.csv",
        mime="text/csv"
    )

    return df_filtrado_verdadeiro, df_filtrado_falso

def main():
    st.title("Ferramenta de Filtragem - Estilo Alteryx")

    df = carregar_dados()

    if df is not None:
        filtrar_dados(df)

if __name__ == "__main__":
    main()
