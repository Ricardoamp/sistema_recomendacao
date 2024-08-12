import pickle
import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados():
    df7 = pd.read_pickle('../data/df7.pkl')
    with open('data/similaridades.pkl', 'rb') as f:
        similaridades = pickle.load(f)
    return df7, similaridades