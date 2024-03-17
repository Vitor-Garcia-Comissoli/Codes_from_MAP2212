#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resumo: Implementacao do algoritmo de Metropolis-Hastings

Autor: Eduardo Janotti Cavalcante         
         
Data: 20 de Maio de 2020
Ultima edicao: 15 de Julho de 2021

"""


import numpy as np
#import matplotlib.pyplot as plt
from datetime import datetime
import math 




def theta(theta1,theta3):
    # funcao potencial
    theta2 = 1 - theta1 - theta3
    if theta1 <0 or theta2<0 or theta3<0:
        return 0
    y = ((theta1**(x1-1))*(theta2**(x2-1))*(theta3**(x3-1)))
    return y
    

def alpha(i,j):
    # alpha de aceitacao utilizado
    if theta(i[0],i[1]) == 0: return 1
    return theta(j[0],j[1])/theta(i[0],i[1])


    
###############################################################################
    
    
def MCMC(aquecimento,tamanho_da_cadeia,saltos,mean,cov,ponto_inicial):
    #gera uma cadeia a partir do n do aquecimento, n do tamanho da cadeia e
    # tamanho dos saltos, matriz de covariancia e ponto inicial
    # funciona apenas para dimensao dois
    
    
    # total de pontos a serem gerados
    n = aquecimento+(tamanho_da_cadeia*saltos)
    
    
    # gera os valores da normal e uniforme anteriormente por vetorizacao
    normal = np.random.multivariate_normal(mean,cov,n)
    uniforme = np.random.uniform(0,1,n)
    
    #contagem dos pontos gerados para pegar o k-esimo candidato
    k = 0
    
    
    #cria a base da cadeia, apenas para facilitar o codigo
    cadeia = [0]*(tamanho_da_cadeia*saltos)

    
    
    
                        #### Aquecimento ####   
    # funcionamento igual ao topico MCMC, sem salvar a cadeia
    # Salvando apenas o ultimo membro
    cadeia_fria = ponto_inicial 
    for i in range(aquecimento):   
        atual = cadeia_fria
        proximo = (0,0)
        caminho = normal[k]
        proximo = (atual[0] + caminho[0] , atual[1] + caminho[1])
        if uniforme[k] < alpha(atual , proximo):
            cadeia_fria = proximo
        k += 1
        
        
        
    # calculo da taxa de aceitacao
    taxa_num = 0
    
            
            
                        #### MCMC ####   
        #######################################################################
    cadeia[0] = cadeia_fria        #A cadeia esquentada recebe o ultimo 
                                     #termo da fria
        #######################################################################
    for i in range((tamanho_da_cadeia*saltos)-1):     
        atual = cadeia[i]    # Posicao atual da cadeia
        #######################################################################
        # Calculo do proximo candidato
        proximo = (0,0)   
        caminho = normal[k]
        proximo = (atual[0] + caminho[0] , atual[1] + caminho[1])
        #######################################################################
                                                   # Decide se a nova posicao é
        if uniforme[k] < alpha(atual , proximo):    # aceita, movendo a 
            cadeia[i+1] = proximo                            # cadeia caso seja 
            
            taxa_num += 1 #calcula a taxa de aceitacao
            
        else:
            #repete o ultimo termo caso n seja aceito
            cadeia[i+1] = atual
            
        k += 1
        #######################################################################  
        
    #taxa de aceitacao
    taxa = taxa_num/len(cadeia)
        
    
    
    if saltos ==1:
        return cadeia,taxa
    
    # elimina parte da amostra para diminuir a correlacao
    cadeia_final = [0]*tamanho_da_cadeia
    for i in range(tamanho_da_cadeia):
        cadeia_final[i] = cadeia[saltos*i]
    return cadeia_final,taxa

    




###############################################################################
###############################################################################
###############################################################################


def u(c,v):
    # calculo de u a partir da cadeia e de um vetor v de cortes, retorna vetor
    soma = [0]*len(v)
    for j in range(len(v)):
        # aqui q entra a ctt de integracao
        k = v[j]/(math.gamma(x1+x2+x3)/(math.gamma(x1)*math.gamma(x2)*math.gamma(x3)))
        for i in c:
            if theta(i[0],i[1]) > k:
                soma[j] += 1
    somas = np.array(soma)
    return 1 - (somas/len(c) )
    
###############################################################################
###############################################################################
###############################################################################
#Definicao dos parametros  
#altere esses valores para testar o codigo
num = 100000   #numero de pontos
x = [4,6,4]  #vetor x
y = [1,2,3]  #vetor y
v = [0,1,0.5,7,15]  # valores a serem calculados


# media da dist normal utilizada
mean = [0,0]
# definificao da matriz de covariancia utilizada
# dimensao 2 pois o terceiro valor eh um menos os outros dois
sigma = 0.02
cov = np.array([[sigma,0],[0,sigma]])
#Ponto inicial da cadeia
ponto_inicial = (0.3,0.3)
saltos = 10
n_cadeia_fria = num//10
###############################################################################

x1,x2,x3 =  [x[0]+y[0],x[1]+y[1],x[2]+y[2]]  # vetor x+y

#calcula o tempo
now1 = datetime.now()

#gera a cadeia
c,taxa = MCMC(n_cadeia_fria,num,saltos,mean,cov,ponto_inicial)   #           

#calcula os u(v)
lista = u(c,v)
    
string = ""
for i in range(len(v)):
    string += f"U({v[i]}) = {lista[i]}\n"
print("As estimativas foram: ")
print(string)

print(f"A taxa de aceitacao foi de {taxa}%")
now2 = datetime.now()
print(f"Programa demorou {now2-now1} para rodar.\n")
print(f"Foram gerados {n_cadeia_fria+(num*saltos)} pontos sendo",
      f"{n_cadeia_fria} o tamanho da cadeia fria e {num*saltos} a",
      f"quantia gerada para se ter uma cadeia de tamanho {num} com",
      f"{saltos} saltos.\n")
print(f"A cadeia se iniciou no ponto {ponto_inicial} e variou a partir",
      "de uma normal multivariada com a seguinte distribuicao:")

string = f"  / |{mean[0]}| |{str(cov[0])[1:-1]}| \\\n"
string+= f"N \ |{mean[1]}|,|{str(cov[1])[1:-1]}| /"
print(string)











    
