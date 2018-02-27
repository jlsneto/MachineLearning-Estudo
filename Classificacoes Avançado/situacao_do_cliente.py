
import pandas as pd
from collections import Counter


#retorna data frames (df) usando pandas
df = pd.read_csv('situacao_do_cliente.csv')

#Retorna data frames das colunas especificadas
X_df = df[['recencia','frequencia','semanas_de_inscricao']]
Y_df = df['situacao']

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

resultados = {}

from sklearn.multiclass import OneVsRestClassifier
#Algoritmo que irá rodar por trás do OneVsRestClassifier
from sklearn.svm import LinearSVC
#random_state roda de maneira fixa e não aleatória
modeloOneVsRest = OneVsRestClassifier(LinearSVC(random_state = 0))
resultadoOneVsRest = fit_and_predict("OneVsRestClassifier",modeloOneVsRest,treino_dados,treino_marcacoes,teste_dados,teste_marcacoes)
#Adiciona ao dicionario
resultados[resultadoOneVsRest] = modeloOneVsRest

from sklearn.multiclass import OneVsOneClassifier
modeloOneVsOne = OneVsOneClassifier(LinearSVC(random_state = 0))
resultadoOneVsOne = fit_and_predict("OneVsOneClassifier",modeloOneVsOne,treino_dados,treino_marcacoes,teste_dados,teste_marcacoes)
resultados[resultadoOneVsOne] = modeloOneVsOne


#testando com MultinomialNB
from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()
resultadoMultinomial = fit_and_predict("MultinomialNB",modeloMultinomial,treino_dados,treino_marcacoes,teste_dados,teste_marcacoes)
resultados[resultadoMultinomial] = modeloMultinomial

#testando com AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier",modeloAdaBoost,treino_dados,treino_marcacoes,teste_dados,teste_marcacoes)
resultados[resultadoAdaBoost] = modeloAdaBoost


maximo = max(resultados)
vencedor = resultados[maximo]
print("Vencedor: ")
print(vencedor)

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




