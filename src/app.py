import ast
import nltk
import sklearn
import numpy as np
import pandas as pd
import streamlit as st

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Carregar os dados
df_raw = pd.read_csv('src/amazon.csv')

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
    recommended_products = [df7.iloc[i[0]].product_name for i in distances[1:6]]
    return recommended_products

# Preparação dos dados
df1 = df_raw.copy()
df2 = df1[['product_id', 'product_name', 'category', 'about_product', 'review_title', 'review_content']]
df3 = df2.drop_duplicates()

df4 = df3.copy()
df4['category'] = df4['category'].apply(lambda x: x.split())
df4['about_product'] = df4['about_product'].apply(lambda x: x.split())
df4['review_title'] = df4['review_title'].apply(lambda x: x.split())
df4['review_content'] = df4['review_content'].apply(lambda x: x.split())

df4['tags'] = df4['category'] + \
              df4['about_product'] + \
              df4['review_title'] + \
              df4['review_content']

df4 = df4[['product_id', 'product_name', 'tags']]
df4['tags'] = df4['tags'].apply(lambda x: " ".join(x))
df4['tags'] = df4['tags'].apply(lambda x: x.lower())

parser_ps = PorterStemmer()
df4['tags'] = df4['tags'].apply(stem)

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df4['tags']).toarray()

similaridades = cosine_similarity(vectors)
df7 = df4.copy()

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
