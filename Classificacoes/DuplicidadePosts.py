import csv

def carregarIdPost(filepath):

    idPost = []

    arquivo = open(filepath,"rt",encoding='utf-8')
    leitor = csv.reader(x.replace('\0', '') for x in arquivo)
    
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

while(1):   
    try:
        filepath = input("Informe o caminho do arquivo .csv (ex. C:/QueryResults.csv):")
        idPost = carregarIdPost(filepath)
        duplicidades = retornaDuplicados(idPost)
        if duplicidades == []:
            print("Sem Post Duplicado!")
        else:
            print("Duplicidades encontradas:")
        for i in duplicidades:
            print(i)

    except:
        print("erro")
    
