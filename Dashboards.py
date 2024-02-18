# Bibliotecas usadas
# a primeira é a que permite criar o dash, a segunda permite manipular os dados e a terceira é a que permite criar os gráficos
import streamlit as st
import pandas as pd
import plotly.express as px

#configuração da página
st.set_page_config(layout='wide')

#### perguntas a serem respondidas com visão mensal
# 1º) Faturamento por mês e por unidade
# 2º) Tipo de produto mais vendido
# 3º) Desempenho das formas de pagamento
# 4º) Avaliação média por filial

#como há uma separação em ; eu coloco sep = ';'
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")

# A data presente em meu df está como string, sendo necessário no caso, converter para um datetime
df['Date'] = pd.to_datetime(df["Date"]) #convertendo para datetime
df = df.sort_values("Date") #ordenar os valores com base na data


#Tendo acesso a quantos meses eu tenho, tornando-o único.
# para isso, pode-se utilizar uma função lambda que é uma função de uma linha apenas
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

#filtrando meu dado
df_filtered = df[df["Month"]== month]

#separando em coluna
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

#gráfico de faturamento por dia com base no mês selecionadado
fig_date = px.bar(df_filtered, x="Date", y="Total", color= "City", title= "Faturamento por dia")
col1.plotly_chart(fig_date)

#gráfico de faturamento por tipo de produto
fig_product = px.bar(df_filtered, x="Date", y="Product line", 
                  color= "City", title= "Faturamento por tipo de produto",
                  orientation="h")
col2.plotly_chart(fig_product)

#contribuição por filial
# criando um df novo e fazendo uma operação de agrupamento para ver o total por filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", 
                  title= "Faturamento por filial")
col3.plotly_chart(fig_city)


#Faturamento por tipo de pagamento por meio de um gráfico de pizza (pie)
fig_kind = px.pie(df_filtered, values="Total", names="Payment", 
                  title= "Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind)


