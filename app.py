import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("ERP Financeiro com Streamlit")
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)

    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)

    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)

    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)

    elif choice == "Relatórios":
        st.subheader("Relatórios Financeiros")  # Subtítulo
        opcao = st.selectbox("Escolha o relatório", ["Fluxo de Caixa por Mês", "Distribuição das Contas a Pagar por Fornecedor", "Status das Contas a Pagar e Receber"])  # Caixa de seleção para escolher o relatório

        # Relatório de Fluxo de Caixa por Mês
        if opcao == "Fluxo de Caixa por Mês":
            df = pd.read_sql_query("""
                SELECT strftime('%Y-%m', data) AS mes,
                       SUM(CASE WHEN tipo='Receita' THEN valor ELSE 0 END) AS receita,
                       SUM(CASE WHEN tipo='Despesa' THEN valor ELSE 0 END) AS despesa
                FROM lancamentos
                GROUP BY mes
            """, conn)  # Consultando os dados para o fluxo de caixa mensal

            plt.figure(figsize=(10, 5))  # Definindo o tamanho do gráfico
            sns.lineplot(x='mes', y='receita', data=df, label='Receita', marker='o')  # Gráfico de receita
            sns.lineplot(x='mes', y='despesa', data=df, label='Despesa', marker='o')  # Gráfico de despesa
            plt.xticks(rotation=45)  # Rotacionando os labels do eixo X
            plt.ylabel('Valor (R$)')  # Rótulo do eixo Y
            plt.xlabel('Mês')  # Rótulo do eixo X
            plt.title('Fluxo de Caixa por Mês')  # Título do gráfico
            plt.legend()  # Legenda do gráfico
            st.pyplot(plt)  # Exibindo o gráfico

        # Relatório de Distribuição das Contas a Pagar por Fornecedor
        elif opcao == "Distribuição das Contas a Pagar por Fornecedor":
            df = pd.read_sql_query("""
                SELECT fornecedor, SUM(valor) AS total
                FROM contas_pagar
                GROUP BY fornecedor
            """, conn)  # Consultando os dados das contas a pagar por fornecedor

            plt.figure(figsize=(8, 8))  # Definindo o tamanho do gráfico
            plt.pie(df['total'], labels=df['fornecedor'], autopct='%1.1f%%', startangle=90)  # Gráfico de pizza
            plt.axis('equal')  # Garantindo que o gráfico de pizza tenha formato circular
            plt.title('Distribuição das Contas a Pagar por Fornecedor')  # Título do gráfico
            st.pyplot(plt)  # Exibindo o gráfico

        # Relatório de Status das Contas a Pagar e Receber
        elif opcao == "Status das Contas a Pagar e Receber":
            df_pagar = pd.read_sql_query("SELECT status, COUNT(*) AS total FROM contas_pagar GROUP BY status", conn)  # Contando o status das contas a pagar
            df_receber = pd.read_sql_query("SELECT status, COUNT(*) AS total FROM contas_receber GROUP BY status", conn)  # Contando o status das contas a receber

            df_pagar['tipo'] = 'Contas a Pagar'  # Adicionando a coluna 'tipo' para identificar as contas a pagar
            df_receber['tipo'] = 'Contas a Receber'  # Adicionando a coluna 'tipo' para identificar as contas a receber
            df_final = pd.concat([df_pagar, df_receber])  # Combinando os dois DataFrames

            plt.figure(figsize=(10, 6))  # Definindo o tamanho do gráfico
            sns.barplot(x='status', y='total', hue='tipo', data=df_final)  # Gráfico de barras com o status
            plt.title('Status das Contas a Pagar e Receber')  # Título do gráfico
            plt.xlabel('Status')  # Rótulo do eixo X
            plt.ylabel('Total')  # Rótulo do eixo Y
            st.pyplot(plt)  # Exibindo o gráfico

    conn.close()  # Fechando a conexão com o banco de dados


if __name__ == "__main__":
    main()
