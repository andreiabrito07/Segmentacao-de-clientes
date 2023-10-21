import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import  TSNE
import datetime as dt
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import  silhouette_score




# Título da página
st.title("         Segmentação de clientes")

# Carregamento do dataset a partir de um arquivo Excel
uploaded_file = st.file_uploader("Carregar o arquivo Excel", type=["xlsx"])
analysis_option = None  

if uploaded_file is not None:
    df_init = pd.read_excel(uploaded_file, engine='openpyxl')

    # Mostrar os dados
    st.write("**Amostra dos dados:**")
    st.dataframe(df_init.head(50))

    # Análise exploratória de dados
    st.write("**Análise Exploratória de Dados**")
    # Resumo estatístico
    st.write("Resumo estatístico dos dados")
    st.write(df_init.describe())

    df_preprocessed = pd.read_excel("./Docs/Datasets/PreProcessedData.xlsx")
    df_preprocessed['Revenue'] = df_preprocessed['Quantity'] * df_preprocessed['Price']

    # Selecionar uma opção de análise exploratória
    analysis_option = st.selectbox(
        "Analise os dados com base nas perguntas abaixo:",
        [
            "Qual a variação das vendas ao longo dos dias?",
            "Qual a variação da receita total por mês?",
            "Qual a variação da quantidade total de produtos vendidos por semana?",
            "Quais os produtos mais vendidos em termos de quantidade e receitas geradas para a empresa?",
            "Quais são os clientes que mais geram receita para a empresa?",
            "Qual é o período de maior atividade de compras?",
            "Quais são os clientes mais ativos e fiéis?",
            "Quais são os países estrangeiros com maior volume de vendas?",
            "Qual é a demanda sazonal dos 10 produtos mais vendidos?",
            "Que tendências, sazonalidades e resíduos podem ser identificados nas vendas da empresa em questão?",

        ]
    )

# Lógica para executar a análise com base na seleção do usuário
if analysis_option == "Qual a variação das vendas ao longo dos dias?":
    # Converter o atributo InvoiceDate para o formato de data
    df_preprocessed['InvoiceDate'] = pd.to_datetime(df_preprocessed['InvoiceDate'])
    df_preprocessed["Customer ID"] = df_preprocessed["Customer ID"].astype(int)
                    
        # Agrupar os dados por dia e calcular a soma das vendas, quantidade de produtos vendidos e receita total para cada dia
    df_por_dia = df_preprocessed.groupby(df_preprocessed['InvoiceDate'].dt.date).agg({
             'Revenue': 'sum',
             'Quantity': 'sum',
              'Price': 'sum'
              })
                    
    # Criar gráfico de linha para visualizar a variação das vendas ao longo dos dias
    fig = plt.figure(figsize=(12, 6))
    plt.plot(df_por_dia.index, df_por_dia['Revenue'])
    plt.xlabel('Data')
    plt.ylabel('Vendas')
    plt.title('Variação das Vendas ao Longo dos Dias')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
    pass
elif analysis_option == "Qual a variação da receita total por mês":
   df_por_mes = df_preprocessed.resample('M', on='InvoiceDate').sum()
   fig = plt.figure(figsize=(12, 6))
   plt.plot(df_por_mes.index, df_por_mes['Price'])
   plt.xlabel('Mês')
   plt.ylabel('Receita Total')
   plt.title('Variação da Receita Total por Mês')
   plt.xticks(rotation=45)
   plt.grid(True)
   plt.show()

   # Mostrar o gráfico no Streamlit
   st.pyplot(fig)
   pass
elif analysis_option == "Qual a variação da quantidade total de produtos vendidos por semana":
    df_por_semana = df_preprocessed.resample('W', on='InvoiceDate').sum()
    fig = plt.figure(figsize=(12, 6))
    plt.bar(df_por_semana.index, df_por_semana['Quantity'])
    plt.xlabel('Semana')
    plt.ylabel('Quantidade de Produtos Vendidos')
    plt.title('Variação da Quantidade de Produtos Vendidos por Semana')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
    pass
elif analysis_option == "Quais os produtos mais vendidos em termos de quantidade e receitas geradas para a empresa?":
   
   
   #Agrupar os dados pelo atributo 'Description' e calcular a quantidade total vendida de cada produto
    quantidade_vendida = df_preprocessed.groupby('Description')['Quantity'].sum().reset_index()
    
    # Ordenar os produtos em ordem decrescente de quantidade vendida
    quantidade_vendida = quantidade_vendida.sort_values(by='Quantity', ascending=False)
    
    # Agrupar os dados pelo atributo 'Description' e calcular a receita total gerada por cada produto
    receita_por_produto = df_preprocessed.groupby('Description')['Revenue'].sum().reset_index()
    
    # Ordenar os produtos em ordem decrescente de receita gerada
    receita_por_produto = receita_por_produto.sort_values(by='Revenue', ascending=False)
    
    print("Produto mais vendido em termos de quantidade: ", quantidade_vendida.head(10))
    
    # Plotar o gráfico das top 10 produtos mais vendidos em termos de quantidade
    fig1 = plt.figure(figsize=(12, 6))
    plt.bar(quantidade_vendida['Description'][:10], quantidade_vendida['Quantity'][:10])
    plt.xlabel('Produto')
    plt.ylabel('Quantidade Vendida')
    plt.title('Top 10 Produtos Mais Vendidos em Termos de Quantidade')
    plt.xticks(rotation=45)
    plt.show()
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig1)

    # Plotar o gráfico das top 10 produtos com maior receita gerada
    fig2 = plt.figure(figsize=(12, 6))
    plt.bar(receita_por_produto['Description'][:10], receita_por_produto['Revenue'][:10])
    plt.xlabel('Produto')
    plt.ylabel('Receita Gerada')
    plt.title('Top 10 Produtos com Maior Receita Gerada')
    plt.xticks(rotation=45)
    plt.show()
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig2)
    pass
elif analysis_option == "Quais são os clientes que mais geram receita para a empresa?":
    
    # Agrupar os dados por cliente e calcular a receita total para cada um
    receita_por_cliente = df_preprocessed.groupby('Customer ID')['Revenue'].sum().reset_index()

    # Ordenar os clientes em ordem decrescente de receita total
    top_clientes_receita = receita_por_cliente.sort_values(by='Revenue', ascending=False)
    
    # Exibir os 10 clientes que mais gastaram em termos de receita total
    top_10_clientes = top_clientes_receita.head(10)
    
    # Adicione a palavra 'client' na frente do ID do cliente para os rótulos
    top_10_clientes.loc[:, 'Customer ID'] = 'CLIENT_ID ' + top_10_clientes['Customer ID'].astype(str)
    
    # Plotar o gráfico de barras invertidas com a receita de cada cliente
    fig = plt.figure(figsize=(10, 6))
    plt.barh(top_10_clientes['Customer ID'], top_10_clientes['Revenue'])
    plt.xlabel('Receita Total')
    plt.title('Receita Gerada por Cliente (Top 10)')
    plt.gca().invert_yaxis()  # Inverter a ordem das barras para ter a maior receita no topo
    plt.show()
   
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
    pass
elif analysis_option == "Qual é o período de maior atividade de compras?":
    
    # Extrair a hora do dia da coluna InvoiceDate
    df_preprocessed['Hour'] = df_preprocessed['InvoiceDate'].dt.hour
        
    # Agrupar os dados por hora do dia e calcular o total de vendas em cada hora
    vendas_por_hora = df_preprocessed.groupby('Hour')['Revenue'].sum()
        
    # Encontrar a hora do dia com maior atividade de compras
    hora_mais_ativa = vendas_por_hora.idxmax()
    total_vendas_hora_mais_ativa = vendas_por_hora.max()
        
    # Exibir a hora do dia com maior atividade de compras e o total de vendas nessa hora
    print(f"Horário de Maior Atividade de Compras: {hora_mais_ativa}h")
    print(f"Total de Vendas nessa Hora: {total_vendas_hora_mais_ativa:.2f}")
        
    # Plotar o gráfico de barras com as vendas por hora do dia
    fig = plt.figure(figsize=(12, 6))
    plt.bar(vendas_por_hora.index, vendas_por_hora)
    plt.xlabel('Hora do Dia')
    plt.ylabel('Receita gerada no horário')
    plt.title('Atividade de Compras por Hora do Dia')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
    pass
elif analysis_option == "Quais são os clientes mais ativos e fiéis?":
    
   # Agrupar por Customer ID e contar o número de transações de cada cliente
    customer_transactions = df_preprocessed.groupby('Customer ID')['Invoice'].nunique().reset_index()
    customer_transactions.rename(columns={'Invoice': 'TransactionCount'}, inplace=True)
        
    # Ordenar o DataFrame pelo total de transações em ordem decrescente
    customer_transactions.sort_values(by='TransactionCount', ascending=False, inplace=True)
        
    # Selecionar os 10 clientes com mais transações
    top_10_customers = customer_transactions.head(10)

    # Adicione a palavra 'client' na frente do ID do cliente para os rótulos
    top_10_customers.loc[:, 'Customer ID'] = 'CLIENT_ID ' + top_10_customers['Customer ID'].astype(str)

    # Plotar gráfico de barras invertidas com os 10 clientes com mais transações
    fig = plt.figure(figsize=(10, 6))
    plt.title('Clientes mais ativos e fiéis (Top 10)')
    plt.barh(top_10_customers['Customer ID'], top_10_customers['TransactionCount'])

    plt.xlabel('Número de Transações')
    plt.ylabel('Cliente')
    plt.show()
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
    pass
elif analysis_option == "Quais são os países estrangeiros com maior volume de vendas?":
    
   # Filtrar as linhas onde o país não seja "United Kingdom"
    non_uk_sales = df_preprocessed[df_preprocessed['Country'] != 'United Kingdom']

    # Agrupar por país e calcular o total de vendas para cada país
    country_sales = non_uk_sales.groupby('Country')['Price'].sum().reset_index()
    country_sales.rename(columns={'Price': 'TotalSales'}, inplace=True)

    # Ordenar o DataFrame pelo total de vendas em ordem decrescente
    country_sales.sort_values(by='TotalSales', ascending=False, inplace=True)

    # Plotar gráfico de barras com os países de maior volume de vendas
    fig = plt.figure(figsize=(12, 6))
    plt.bar(country_sales['Country'], country_sales['TotalSales'])
    plt.xlabel('País')
    plt.ylabel('Total de vendas')
    plt.title('Países com maior volume de vendas (excluindo o Reino Unido)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
    pass
elif analysis_option ==  "Qual é a demanda sazonal dos 10 produtos mais vendidos?":
    
   # Converter a coluna InvoiceDate para o tipo datetime
    df_preprocessed['InvoiceDate'] = pd.to_datetime(df_preprocessed['InvoiceDate'])

    # Criar colunas para o mês e o ano da transação
    df_preprocessed['Month'] = df_preprocessed['InvoiceDate'].dt.month
    df_preprocessed['Year'] = df_preprocessed['InvoiceDate'].dt.year

    # Agrupar por produto e mês para calcular a demanda sazonal
    product_monthly_demand = df_preprocessed.groupby(['Description', 'Month'])['Quantity'].sum().reset_index()

    # Calcular o total de vendas para cada produto
    product_total_sales = df_preprocessed.groupby('Description')['Quantity'].sum().reset_index()

    # Filtrar apenas os produtos com maior demanda
    top_products = product_total_sales.nlargest(10, 'Quantity')['Description']

    # Filtrar os dados apenas para os produtos com maior demanda
    product_monthly_demand_top = product_monthly_demand[product_monthly_demand['Description'].isin(top_products)]

    # Plotar gráfico de linhas para mostrar a demanda sazonal dos produtos com maior demanda
    fig = plt.figure(figsize=(16, 18))
    sns.lineplot(data=product_monthly_demand_top, x='Month', y='Quantity', hue='Description', marker='o')
    plt.xlabel('Mês')
    plt.ylabel('Demanda mensal')
    plt.title('Tendência de Demanda Sazonal dos Produtos com Maior Demanda')
    plt.xticks(range(1, 13), ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    plt.tight_layout()
    plt.legend(title='Produtos', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
    pass
elif analysis_option ==   "Que tendências, sazonalidades e resíduos podem ser identificados nas vendas da empresa em questão?":
    
   # Agrupar os dados por data e calcular a receita total (ou outra métrica de interesse)
    df_por_data = df_preprocessed.groupby(df_preprocessed['InvoiceDate'].dt.date).agg({
            'Revenue': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
    # Configurar a coluna de data como índice do DataFrame
    df_por_data.set_index('InvoiceDate', inplace=True)
        
    # Verificar se o índice é do tipo DatetimeIndex
    if not isinstance(df_por_data.index, pd.DatetimeIndex):
        df_por_data.index = pd.to_datetime(df_por_data.index)
        
    # Calcular a tendência (média móvel de 7 dias)
    trend = df_por_data['Revenue'].rolling(window=7, center=True).mean()
        
    # Calcular a sazonalidade (diferença entre os dados e a tendência)
    seasonal = df_por_data['Revenue'] - trend
        
    # Calcular os resíduos (dados - tendência - sazonalidade)
    residual = df_por_data['Revenue'] - trend - seasonal
        
    # Calcular a incerteza (desvio padrão da média móvel de 7 dias)
    rolling_std = df_por_data['Revenue'].rolling(window=7, center=True).std()
        
    # Plotar os componentes da decomposição
    fig = plt.figure(figsize=(15, 12))
        
    # Tendência
    plt.subplot(4, 1, 1)
    plt.plot(trend, label='Tendência')
    plt.xlabel('Data')
    plt.ylabel('Tendência')
    plt.legend()
    plt.title('Tendência da Receita Total')
        
    # Sazonalidade
    plt.subplot(4, 1, 2)
    plt.plot(seasonal, label='Sazonalidade')
    plt.xlabel('Data')
    plt.ylabel('Sazonalidade')
    plt.legend()
    plt.title('Sazonalidade da Receita Total')
        
    # Resíduos com incerteza
    plt.subplot(4, 1, 3)
    plt.plot(residual, label='Resíduos', color='gray')
    plt.fill_between(df_por_data.index, -rolling_std, rolling_std, color='gray', alpha=0.2, label='Incerteza (Resíduos)')
    plt.xlabel('Data')
    plt.ylabel('Resíduos')
    plt.legend()
    plt.title('Resíduos da Receita Total com Incerteza')
        
    # Série Temporal Original
    plt.subplot(4, 1, 4)
    plt.plot(df_por_data['Revenue'], label='Receita Total', color='gray')
    plt.xlabel('Data')
    plt.ylabel('Receita Total')
    plt.legend()
    plt.title('Série Temporal Original')
        
    plt.tight_layout()
    plt.show()
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
    pass

#_____________________________________________________________________VISUALIZAÇÃO DOS CLUSTERS E INTERPRETAÇÃO________________________________________________#
# Mostrar os dados
st.write("**CLUSTERS GERADOS**")
final_df = pd.read_excel('./Docs/Datasets/final_df.xlsx')

kmeans = KMeans(init='k-means++', n_clusters=8, random_state=0)

kmeans.fit(final_df)

#Clusters gerados
clusters = kmeans.predict(final_df)

#Reduzir dimensionalidade do final_df para duas dimensões
tsne = TSNE(n_components=2)
proj = tsne.fit_transform(final_df)

#Dimensões do grafico
w = proj[:,0]
h = proj[:,1]

#Plotar gráfico dos clusters
fig_clusters = plt.figure(figsize=(10,10))
plt.scatter(w, h, c=clusters)
plt.title("Visualização dos clusters", fontsize='18')

# Mostrar o gráfico no Streamlit
st.pyplot(fig_clusters)

#_________________________________________________________________ANÁLISE DE CLUSTERS _____________________________________________________________________#

final_dataset = pd.read_excel('./Docs/Datasets/DatasetClusterizado_K_Means.xlsx')
df_aux =  pd.read_excel('./Docs/Datasets/CustomerBehaviour.xlsx')

for cluster_num in range(8):
    df_temporario= final_dataset.reset_index()
    st.write(f"Análise Cluster {cluster_num}")

    cust = list(df_temporario[df_temporario['cluster'] == cluster_num]['Customer ID'])
    current_cluster = df_aux[df_aux['Customer ID'].isin(cust)]

    st.write(current_cluster[['Quantity', 'Price', 'Revenue', 'frequency', 'min_recency', 'monetary_value']].mean())
    
    # Obter a contagem dos valores e pegue os 10 mais frequentes
    top_10_descriptions = current_cluster['Description'].value_counts().head(10)

    # Criar um DataFrame a partir dos resultados
    top_10_df = pd.DataFrame({'Description': top_10_descriptions.index, 'Count': top_10_descriptions.values})

    # Exibir o DataFrame em forma de tabela
    st.write(top_10_df)

    
    # Definir as funções de agregação
    customer_aggregation = {}
    customer_aggregation['Country'] = lambda x: x.iloc[0]
    customer_aggregation['RFMScore'] = lambda x: x.iloc[0]

    # Agrupar os dados pelo 'Customer ID' e aplicar as funções de agregação
    cluster_grouped = current_cluster.groupby('Customer ID').agg(customer_aggregation)

    # Calcular a contagem dos valores únicos na coluna 'RFMScore'
    rfm_score_counts = cluster_grouped['RFMScore'].value_counts()

    # Criar um DataFrame a partir dos resultados
    rfm_score_df = pd.DataFrame({'RFMScore': rfm_score_counts.index, 'Count': rfm_score_counts.values})

    # Exibir o DataFrame em forma de tabela no Streamlit
    st.write(rfm_score_df)
