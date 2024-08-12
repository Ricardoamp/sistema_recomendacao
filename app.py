import streamlit as st
from src.recomendacao import sistema_recomendacao
import pickle

# Carregar os dados previamente salvos
with open('data/df7.pkl', 'rb') as f:
    df7 = pickle.load(f)

with open('data/similaridades.pkl', 'rb') as f:
    similaridades = pickle.load(f)

# Configurar o aplicativo Streamlit
st.title('Sistema de Recomendação de Produtos')

# Menu lateral
opcao = st.sidebar.selectbox('Escolha um produto', df7['product_name'])

# Exibir recomendações
st.write(f'Recomendações para {opcao}:')

# Obter e exibir recomendações
recomendacoes = sistema_recomendacao(opcao, df7, similaridades)
for produto in recomendacoes:
    st.write(produto)
