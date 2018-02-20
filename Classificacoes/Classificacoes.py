#gordo?, curta?, late?
#1 para sim e 0 para não
porco1 = [1,1,0]
porco2 = [1,1,0]
porco3 = [1,1,0]
cachorro1 = [1,1,1]
cachorro2 = [0,1,1]
cachorro3 = [0,1,1]

dados = [porco1, porco2, porco3,
         cachorro1,cachorro2,cachorro3]

#marcar os dados, 1 porco e -1 cachorro
marcacoes = [1,1,1,-1,-1,-1]

#baseado nos dados e marcações treina-se o algoritmo

#algoritmo usado para treinar o modelo
from sklearn.naive_bayes import MultinomialNB

modelo = MultinomialNB()

#treinar
modelo.fit(dados, marcacoes)

misterioso1 = [1,1,1]
misterioso2 = [1,0,0]
misterioso3 = [0,1,1]

testes = [misterioso1,misterioso2,misterioso3]

#predizer
resposta = modelo.predict(testes)

#valor esperado
marcacoes_teste = [-1, 1, -1]

diferencas = resposta - marcacoes_teste

acertos = [i for i in diferencas if i == 0]
erros = [i for i in diferencas if i != 0]

totalAcertos = len(acertos)
totalElementos = len(testes)

taxaAcerto = (totalAcertos/totalElementos)*100

for i in resposta:
    if(i == 1):
        print("Porco")
    else:
        print("Cachorro")

print("Taxa de Acertos",taxaAcerto)
