import streamlit as st
from src.load_data import carregar_dados
from src.recomendacao import sistema_recomendacao

# Carregar os dados
df7, similaridades = carregar_dados()

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