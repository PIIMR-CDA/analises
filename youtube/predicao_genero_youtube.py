import pandas as pd
from csv import writer


def consulta_genero(dados, nome):
    '''
    Consulta o nome no DataFrame para verificar a distribuica de genero para
    esse nome no Brasil. Retorna uma tupla com o genero mais recorrente e a
    frequencia desse genero mais recorrente para aquele nome 
    '''
    try:
        query = dados.where(dados['first_name'] == nome.upper())

        genero = query['classification'].dropna().to_list()[0]

        # A base de dados possui uma coluna "ratio" com a frequencia do genero para
        # determinado nome. Porem os resultados nao estao normalizados e parecem 
        # caoticos. Portanto, vamos usar outros dados da base para determinar isso
        if genero == 'F':
            frequencia_genero = int(query['frequency_female'].dropna().to_list()[0])
        elif genero == 'M':
            frequencia_genero = int(query['frequency_male'].dropna().to_list()[0])

        frequencia_total = int(query['frequency_total'].dropna().to_list()[0])
        frequencia = frequencia_genero / frequencia_total

        resultado = (genero, frequencia)
        return resultado

    except:
        return (None, None)


dados_genero =  pd.read_csv('/home/vitor/Desktop/Coleta-CDA/data/genero_nomes.csv')
comentarios = pd.read_csv("/home/vitor/Downloads/coleta_youtube/coleta1/comentarios/comentarios1.csv")

comentarios["genero"] = ""
comentarios["distribuicao genero"] = ""


for index in comentarios.index:
    primeiro_nome =  comentarios.at[index, "author"].split()[0]

    (genero, ratio) = consulta_genero(dados_genero, primeiro_nome)

    if (genero and ratio) != None:
        comentarios.at[index, "genero"] = genero
        comentarios.at[index, "distribuicao genero"] = ratio


comentarios.to_csv("/home/vitor/Downloads/coleta_youtube/coleta1/comentarios/comentarios1_genero.csv", encoding="utf-8")