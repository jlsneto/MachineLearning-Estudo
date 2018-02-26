#Minha regra inicial foi
#1 - separar 10% para teste e 90% para treino
#resultado: 88.89% acertos
import pandas as pd
from collections import Counter
#retorna data frames (df) usando pandas
df = pd.read_csv('busca.csv')

#Retorna data frames das colunas especificadas
X_df = df[['home','busca','logado']]
Y_df = df['comprou']

#retorna a categorização (dummies). Ainda é data frames
Xdummies_df = pd.get_dummies(X_df)

Ydummies_df = Y_df

#retornar Arrays das dummies
X = Xdummies_df.values
Y = Ydummies_df.values


#retorna 90% da quantidade de marcações
tamanho_de_treino = 0.9 * len(Y)

#retorna 10% da quantidade de marcações
tamanho_de_teste = len(Y) - tamanho_de_treino

#primeiros 90% de dados
treino_dados = X[:int(tamanho_de_treino)]
#primeiros 90% de marcações
treino_marcacoes = Y[:int(tamanho_de_treino)]

#últimos 10% dos dados para teste
teste_dados = X[-int(tamanho_de_teste):]
#ultimos 10% das marcações para teste
teste_marcacoes = Y[-int(tamanho_de_teste):]


from sklearn.naive_bayes import MultinomialNB
modelo = MultinomialNB()

#treinar
modelo.fit(treino_dados,treino_marcacoes)

#predizer
#Mandando os mesmos dados para testar
resposta = modelo.predict(teste_dados)

acertos = (resposta==teste_marcacoes)

#soma os true, pois são em python true é 1 e false é 0
total_acertos = sum(acertos)

total_elementos = len(teste_dados)

taxa_acertos = (total_acertos/total_elementos)*100.0

print("Taxa de Acerto %.2f" %(taxa_acertos))

print("Total Registros Testados: %.2f" %(total_elementos))


#eficácia do algoritmo que chuta tudo
acerto_base = max(Counter(teste_marcacoes).values())
taxa_de_acerto_base = (acerto_base/len(teste_marcacoes))*100
print("Taxa de acerto base: %.2f" %(taxa_de_acerto_base))





