import csv

def carregarAcessos():

    X = []
    Y = []

    arquivo = open("acesso.csv","rt")
    print("lendo arquivo...")
    leitor = csv.reader(arquivo)

    #pular primeira linha
    next(leitor)
    
    for acessou_home,acessou_como_funciona,acessou_contato,comprou in leitor:
            dado = [int(acessou_home),
                          int(acessou_como_funciona),
                         int(acessou_contato)]
            X.append(dado)
            Y.append(int(comprou))
            
    print("finalizado!")
    
    return X,Y
    
        
def carregarBuscas():

    X = []
    Y = []

    arquivo = open("busca.csv","rt")
    print("lendo arquivo...")
    leitor = csv.reader(arquivo)

    next(leitor)

    for acessou_home,busca,logado,comprou in leitor:
        dado = [int(acessou_home),busca,int(logado)]
        X.append(dado)
        Y.append(int(comprou))

    return X, Y
