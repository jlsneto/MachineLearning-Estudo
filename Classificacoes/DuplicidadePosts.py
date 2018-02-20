import csv

def carregarIdPost():

    idPost = []

    arquivo = open("QueryResults.csv","rt",encoding="utf8")
    leitor = csv.reader(arquivo)

    #pular primeira linha
    next(leitor)

    for Id,Title,Score,Tags,Text,CreationDate in leitor:
        idPost.append(Id)

    return idPost

def retornaDuplicados(idPost):
    unico = []
    duplicados = []
    for x in idPost:

        if x not in unico:
            unico.append(x)
        else:
            if x not in repetido:
                duplicados.append(x)
    return duplicados
    
    
