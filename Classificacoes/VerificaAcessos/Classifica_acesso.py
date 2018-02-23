#Minha regra inicial foi
#1 - separar 10% para teste e 90% para treino
#resultado: 88.89% acertos


from Dados import carregarAcessos

#X -> Dados
#Y -> Marcações
X,Y = carregarAcessos()

#primeiras noventa linhas
print("carregando dados para treino")
treino_dados = X[:90]
print("carregando marcacoes para teste")
treino_marcacoes = Y[:90]

#ultimas nove linhas
print("carregando dados para teste")
teste_dados = X[-9:]
print("carregando marcações para teste")
teste_marcacoes = Y[-9:]



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
