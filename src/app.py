import ast
import nltk
import sklearn
import numpy as np
import pandas as pd
import streamlit as st

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

parser_ps = PorterStemmer()

# Função para carregar os dados com cache para melhorar o desempenho
@st.cache_data
def carregar_dados():
    return pd.read_csv('src/amazon.csv')

# Carregar os dados
df_raw = carregar_dados()

# Função stemming
def stem(text):
    y = []
    for i in text.split():
        y.append(parser_ps.stem(i))
    return " ".join(y)

# Função para o sistema de recomendação
def sistema_recomendacao(movie):
    index = df7[df7['product_name'] == movie].index[0]
    distances = sorted(list(enumerate(similaridades[index])), reverse=True, key=lambda x: x[1])
    recommended_products = [df7.iloc[i[0]].product_name for i in distances[1:4]]  # Exibir apenas 3 recomendações
    return recommended_products

# Preparação dos dados
df1 = df_raw[['product_id', 'product_name', 'category', 'about_product', 'review_title', 'review_content']].drop_duplicates()

df1['tags'] = (df1['category'] + ' ' + df1['about_product'] + ' ' + df1['review_title'] + ' ' + df1['review_content']).apply(lambda x: x.split())

df1['tags'] = df1['tags'].apply(lambda x: " ".join(x).lower())
df1['tags'] = df1['tags'].apply(stem)

# Função para calcular as similaridades com cache
@st.cache_resource
def calcular_similaridades(vectors):
    return cosine_similarity(vectors)

# Vectorização e cálculo das similaridades
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df1['tags']).toarray()
similaridades = calcular_similaridades(vectors)

df7 = df1.copy()

# Configurar o aplicativo Streamlit
st.title('Sistema de Recomendação de Produtos')

# Menu lateral
opcao = st.sidebar.selectbox('Escolha um produto', df7['product_name'])

# Exibir recomendações
st.write(f'Recomendações para {opcao}:')

# Obter e exibir recomendações
recomendacoes = sistema_recomendacao(opcao)
for produto in recomendacoes:
    st.write(produto)
