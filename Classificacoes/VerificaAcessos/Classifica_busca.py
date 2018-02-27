#Minha regra inicial foi
#1 - separar 10% para teste e 80% para treino e ultimos 10% para validação
#Taxa de Acerto do MultinomialNB: 82.0
#Taxa de Acerto do AdaBoostClassifier: 84.0
#Taxa de Acerto do Vencedor entre os dois algoritmos no mundo real: 85.0
#Taxa de acerto base o 'burro': 82.00
#Total Registros Testados: 100

import pandas as pd
from collections import Counter

# teste inicial: home, busca, logado -> comprou
#home, busca
#busca, logado
#busca: 85.71% (7 testes)

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


#distribui os dados para treino, teste e validação
tamanho_de_treino = 0.8 * len(Y)
tamanho_de_teste = 0.1 * len(Y)
tamanho_de_validacao = len(Y) - tamanho_de_treino - tamanho_de_teste


#primeiros 80% de dados
treino_dados = X[0:int(tamanho_de_treino)]
#primeiros 80% de marcações
treino_marcacoes = Y[0:int(tamanho_de_treino)]

fim_de_teste = int(tamanho_de_treino+tamanho_de_teste)

#próximos 10% dos dados para teste
teste_dados = X[int(tamanho_de_treino):fim_de_teste]
#próximos 10% das marcações para teste
teste_marcacoes = Y[int(tamanho_de_treino):fim_de_teste]

#ultimos 10% para treino "na vida real"
validacao_dados = X[fim_de_teste:]
validacao_marcacoes = Y[fim_de_teste:]

#validação

def fit_and_predict(nome,modelo,treino_dados,treino_marcacoes,teste_dados,teste_marcacoes):        
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

    msg = "Taxa de Acerto do {0}: {1}".format(nome,taxa_acertos)
    print(msg)
    
    return taxa_acertos

#testando com MultinomialNB
from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()
resultadoMultinomial = fit_and_predict("MultinomialNB",modeloMultinomial,treino_dados,treino_marcacoes,teste_dados,teste_marcacoes)

#testando com AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier",modeloAdaBoost,treino_dados,treino_marcacoes,teste_dados,teste_marcacoes)

if(resultadoMultinomial > resultadoAdaBoost):
    vencedor = modeloMultinomial
else:
    vencedor = modeloAdaBoost

resultado = vencedor.predict(validacao_dados)

acertos = (resultado==validacao_marcacoes)

#soma os true, pois são em python true é 1 e false é 0
total_acertos = sum(acertos)

total_elementos = len(validacao_marcacoes)

taxa_acertos = (total_acertos/total_elementos)*100.0

msg = "Taxa de Acerto do Vencedor entre os dois algoritmos no mundo real: {0}".format(taxa_acertos)
print(msg)

#eficácia do algoritmo que chuta tudo
acerto_base = max(Counter(validacao_marcacoes).values())
taxa_de_acerto_base = (acerto_base/len(validacao_marcacoes))*100
print("Taxa de acerto base o 'burro': %.2f" %(taxa_de_acerto_base))
print("Total Registros Testados: %d" %(len(validacao_dados)))




