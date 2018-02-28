import pandas as pd
from collections import Counter
import numpy as np
from sklearn.model_selection import cross_val_score

classificacoes = pd.read_csv('emails.csv')
textosPuros = classificacoes['email']
#transfomar os textos puros tudo em string lowercase e divide pelo espaço
textosQuebrados = textosPuros.str.lower().str.split(' ')

#dicionário que só irá receber valores únicos
dicionario = set()
for lista in textosQuebrados:
    dicionario.update(lista)

totalDePalavras = len(dicionario)
#adiciona numeração para cada palavra e depois transforma em um dicionario
tradutor = dict(zip(dicionario, range(totalDePalavras)))

#cria vetor e preenche o vetor com o número de ocorrências da palavra
def vetorizar_texto(texto, tradutor):
    vetor = [0] * len(tradutor)

    for palavra in texto:
        if palavra in tradutor:
            posicao = tradutor[palavra]
            vetor[posicao] +=1
            
    return vetor



#vetoriza todos os textos
vetoresDeTexto = [vetorizar_texto(texto, tradutor) for texto in textosQuebrados]

marcas = classificacoes['classificacao']

X = np.array(vetoresDeTexto)
Y = marcas


#distribui os dados para treino, teste e validação
porcentagem_de_treino = 0.8

tamanho_de_treino = porcentagem_de_treino * len(Y)
tamanho_de_validacao = len(Y) - tamanho_de_treino

#primeiros 80% de dados
treino_dados = X[0:int(tamanho_de_treino)]
#primeiros 80% de marcações
treino_marcacoes = Y[0:int(tamanho_de_treino)]

#ultimos 10% para treino "na vida real"
validacao_dados = X[int(tamanho_de_treino):]
validacao_marcacoes = Y[int(tamanho_de_treino):]


def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes):
    #precisamos fazer o k-fold
    #quebra em 3 pedaços
    k = 10
    scores = cross_val_score(modelo, treino_dados, treino_marcacoes, cv = k)
    taxa_de_acerto = np.mean(scores)

    msg = "Taxa de acerto do {0}: {1}".format(nome, taxa_de_acerto)
    print(msg)
    return taxa_de_acerto

resultados = {}

from sklearn.multiclass import OneVsRestClassifier
#Algoritmo que irá rodar por trás do OneVsRestClassifier
from sklearn.svm import LinearSVC
#random_state roda de maneira fixa e não aleatória
modeloOneVsRest = OneVsRestClassifier(LinearSVC(random_state = 0))
resultadoOneVsRest = fit_and_predict("OneVsRestClassifier",modeloOneVsRest,treino_dados,treino_marcacoes)
#Adiciona ao dicionario
resultados[resultadoOneVsRest] = modeloOneVsRest

from sklearn.multiclass import OneVsOneClassifier
modeloOneVsOne = OneVsOneClassifier(LinearSVC(random_state = 0))
resultadoOneVsOne = fit_and_predict("OneVsOne", modeloOneVsOne, treino_dados, treino_marcacoes)
resultados[resultadoOneVsOne] = modeloOneVsOne

from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()
resultadoMultinomial = fit_and_predict("MultinomialNB",modeloMultinomial,treino_dados,treino_marcacoes)
resultados[resultadoMultinomial] = modeloMultinomial

#testando com AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier",modeloAdaBoost,treino_dados,treino_marcacoes)
resultados[resultadoAdaBoost] = modeloAdaBoost

#verifica quem foi o melhor, vendo o maior resultado
maximo = max(resultados)
#grava o modelo vencedor
vencedor = resultados[maximo]
print("Vencedor: ")
print(vencedor)

vencedor.fit(treino_dados, treino_marcacoes)
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


