import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recomendacao import sistema_recomendacao

# Carregar os dados
df_raw = pd.read_csv('data/amazon.csv')

# Função para preparar os dados
def preparar_dados(df_raw):
    df1 = df_raw[['product_id', 'product_name', 'category', 'about_product', 'review_title', 'review_content']].drop_duplicates()
    df1['tags'] = (df1['category'] + ' ' + df1['about_product'] + ' ' + df1['review_title'] + ' ' + df1['review_content']).apply(lambda x: x.split())
    df1['tags'] = df1['tags'].apply(lambda x: " ".join(x).lower())
    return df1

# Preparar os dados
df1 = preparar_dados(df_raw)

# Vectorização e cálculo das similaridades
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df1['tags']).toarray()
similaridades = cosine_similarity(vectors)

df7 = df1.copy()

# Salvar os arquivos
with open('data/df7.pkl', 'wb') as f:
    pickle.dump(df7, f)

with open('data/similaridades.pkl', 'wb') as f:
    pickle.dump(similaridades, f)

with open('data/cv.pkl', 'wb') as f:
    pickle.dump(cv, f)