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
    
        
