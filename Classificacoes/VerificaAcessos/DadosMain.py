from Dados import carregarAcessos

#X -> Dados
#Y -> Marcações
X,Y = carregarAcessos()

from sklearn.naive_bayes import MultinomialNB

modelo = MultinomialNB()

#treinar
modelo.fit(X,Y)

#predizer
#Mandando os mesmos dados para testar
resposta = modelo.predict(X)

#Utilizando os valores originais como teste
diferencas = resposta - Y

# se a diferença for 0, então grava
acertos = [i for i in diferencas if i == 0]

total_acertos = len(acertos)

total_elementos = len(X)

taxa_acertos = (total_acertos/total_elementos)*100.0

print("Taxa de Acerto %f" %(taxa_acertos))

print("Total Registros Testados: %d" %(total_elementos))
