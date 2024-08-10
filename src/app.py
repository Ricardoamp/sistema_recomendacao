import ast
import nltk
import sklearn
import numpy as np
import pandas as pd
import streamlit as st

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df_raw = pd.read_csv('amazon.csv')

# Função stemming
def stem(text):
  y=[]
  for i in text.split():
    y.append(parser_ps.stem(i))
  return " ".join(y)

# Função para o sistema de recomendação
def sistema_recomendacao(movie):
  index = df7[df7['product_name'] == movie].index[0]
  distances = sorted(list(enumerate(similaridades[index])), reverse=True, key=lambda x:x[1])

  for i in distances[1:6]:
    print(df7.iloc[i[0]].product_name)


df1 = df_raw.copy()
df2 = df1.copy()
df2 = df2[['product_id', 'product_name', 'category', 'about_product', 'review_title', 'review_content']]
df3 = df2.copy()
df3 = df3.drop_duplicates()
df4 = df3.copy()
df4['category'] = df4['category'].apply(lambda x:x.split())
df4['about_product'] = df4['about_product'].apply(lambda x:x.split())
df4['review_title'] = df4['review_title'].apply(lambda x:x.split())
df4['review_content'] = df4['review_content'].apply(lambda x:x.split())

df4['tags'] = df4['category'] + \
              df4['about_product'] + \
              df4['review_title'] + \
              df4['review_content']


df4 = df4[['product_id', 'product_name', 'tags']]
df4['tags'] = df4['tags'].apply(lambda x:" ".join(x))
df4['tags'] = df4['tags'].apply(lambda x:x.lower())
df5 = df4.copy()

parser_ps = PorterStemmer()
df5['tags'] = df5['tags'].apply(stem)
atributos = 5000
cv = CountVectorizer(max_features=atributos, stop_words='english')
vectors = cv.fit_transform(df5['tags']).toarray()
df6 = df5.copy()
similaridades = cosine_similarity(vectors)
df7 = df6.copy()

# Configurar o aplicativo Streamlit
st.title('Sistema de Recomendação de Produtos')

# Menu lateral
opcao = st.sidebar.selectbox('Escolha um produto', df7['Produto'])

# Exibir recomendações
st.write(f'Recomendações para o {opcao}:')

# Obter e exibir recomendações
recomendacoes = sistema_recomendacao(opcao)
st.write(', '.join(recomendacoes))