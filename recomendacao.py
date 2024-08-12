def sistema_recomendacao(movie, df7, similaridades):
    index = df7[df7['product_name'] == movie].index[0]
    distances = sorted(list(enumerate(similaridades[index])), reverse=True, key=lambda x: x[1])
    recommended_products = [df7.iloc[i[0]].product_name for i in distances[1:4]]  # Exibir apenas 3 recomendações
    return recommended_products