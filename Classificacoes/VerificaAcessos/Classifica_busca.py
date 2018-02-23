#Minha regra inicial foi
#1 - separar 10% para teste e 90% para treino
#resultado: 88.89% acertos
import pandas as pd

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

diferencas = resposta - teste_marcacoes

# se a diferença for 0, então grava
acertos = [i for i in diferencas if i == 0]

total_acertos = len(acertos)

total_elementos = len(teste_dados)

taxa_acertos = (total_acertos/total_elementos)*100.0

print("Taxa de Acerto %f" %(taxa_acertos))

print("Total Registros Testados: %d" %(total_elementos))







