import streamlit as st
import pandas as pd
import io

def criar_tabela_manual():
    """Cria uma interface para inserir dados manualmente e gerar arquivos"""
    
    st.title("Ferramenta de Entrada de Texto - Estilo Alteryx")

    # Definir os nomes das colunas
    colunas = st.text_area("Digite os nomes das colunas separados por vírgula", "Nome, Idade, Cidade")
    
    # Processar os nomes das colunas
    colunas = [col.strip() for col in colunas.split(",") if col.strip()]

    if not colunas:
        st.warning("Por favor, insira pelo menos uma coluna válida.")
        return

    # Criar um DataFrame vazio com as colunas definidas
    df = pd.DataFrame(columns=colunas)

    # Criar um campo para entrada de dados manual
    st.write("Insira os dados manualmente abaixo (separados por vírgula para cada linha):")
    dados_texto = st.text_area("Exemplo: João, 30, São Paulo\nMaria, 25, Rio de Janeiro")

    # Processar entrada de dados
    if dados_texto:
        linhas = [linha.split(",") for linha in dados_texto.strip().split("\n")]
        df = pd.DataFrame(linhas, columns=colunas)

    # Exibir a tabela editável
    st.write("Tabela Gerada:")
    st.dataframe(df)

    # Botão para baixar CSV
    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Baixar como CSV", csv, "entrada_texto.csv", "text/csv")

        # Baixar como Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        st.download_button("Baixar como Excel", output.getvalue(), "entrada_texto.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

def main():
    criar_tabela_manual()

if __name__ == "__main__":
    main()
