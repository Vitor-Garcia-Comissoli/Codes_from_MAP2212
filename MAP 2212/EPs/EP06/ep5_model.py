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

class MCMC:
    def __init__(self, num=100000, x=np.array([4,6,4]), y=np.array([1,2,3]),
                 v=np.array([0,1,0.5,7,15]), saltos=10, n_cadeia_fria=10000):
        self.num = num   #numero de pontos
        self.x = x  #vetor x
        self.y = y  #vetor y
        self.v = v  # valores a serem calculados
        self.saltos = saltos
        self.n_cadeia_fria = n_cadeia_fria
        self.x1 =  x[0] + y[0]
        self.x2 = x[1] + y[1]
        self.x3 = x[2] + y[2]  # vetor x+y
        self.cadeia = np.array([])

    def theta(self, theta1, theta3):
        # funcao potencial
        theta2 = 1 - theta1 - theta3
        if theta1 < 0 or theta2 < 0 or theta3 < 0:
            return 0
        y = ((theta1 ** (self.x1 - 1)) *
                (theta2 ** (self.x2 - 1)) * (theta3 ** (self.x3 - 1)))
        return y

    def alpha(self, i, j):
        # alpha de aceitacao utilizado
        if self.theta(i[0], i[1]) == 0:
            return 1
        return self.theta(j[0], j[1]) / self.theta(i[0], i[1])

###############################################################################
    
    
    def run_MCMC(self, aquecimento, tamanho_da_cadeia, saltos, mean, cov, ponto_inicial):
        # gera uma cadeia a partir do n do aquecimento, n do tamanho da cadeia e
        # tamanho dos saltos, matriz de covariancia e ponto inicial
        # funciona apenas para dimensao dois
        
        
        # total de pontos a serem gerados
        n = aquecimento + (tamanho_da_cadeia * saltos)
        
        
        # gera os valores da normal e uniforme anteriormente por vetorizacao
        normal = np.random.multivariate_normal(mean, cov, n)
        uniforme = np.random.uniform(0, 1, n)
        
        #contagem dos pontos gerados para pegar o k-esimo candidato
        k = 0
        
        
        cadeia = np.zeros((tamanho_da_cadeia * saltos, 2))
        
                            #### Aquecimento ####   
        # funcionamento igual ao topico MCMC, sem salvar a cadeia
        # Salvando apenas o ultimo membro
        cadeia_fria = ponto_inicial 
        for i in range(aquecimento):   
            atual = cadeia_fria
            caminho = normal[k]
            proximo = atual + caminho
            if uniforme[k] < self.alpha(atual , proximo):
                cadeia_fria = proximo
            k += 1
            
        # calculo da taxa de aceitacao
        taxa_num = 0
        
                
        cadeia[0, :] = cadeia_fria        #A cadeia esquentada recebe o ultimo 
                                         #termo da fria
        for i in range((tamanho_da_cadeia*saltos) - 1):     
            atual = cadeia[i]    # Posicao atual da cadeia
            # Calculo do proximo candidato
            #proximo = (0,0)   
            caminho = normal[k]
            proximo = atual + caminho
                                                       # Decide se a nova posicao é
            if uniforme[k] < self.alpha(atual, proximo):    # aceita, movendo a 
                cadeia[i+1] = proximo                            # cadeia caso seja 
                
                taxa_num += 1 #calcula a taxa de aceitacao
                
            else:
                #repete o ultimo termo caso n seja aceito
                cadeia[i+1] = atual
                
            k += 1
            
        #taxa de aceitacao
        taxa = taxa_num / cadeia.shape[0]
            
        
        
        if saltos == 1:
            self.cadeia = cadeia
            return taxa
        
        # elimina parte da amostra para diminuir a correlacao
        #cadeia_final = [0] * tamanho_da_cadeia
        cadeia_final = np.zeros((tamanho_da_cadeia, 2))
        for i in range(tamanho_da_cadeia):
            cadeia_final[i] = cadeia[saltos * i]
        self.cadeia = cadeia_final
        return taxa


    def u(self, c, v):
        # calculo de u a partir da cadeia e de um vetor v de cortes, retorna vetor
        #soma = [0] * len(v)
        soma = np.zeros(len(v))
        for j in range(len(v)):
            # aqui q entra a ctt de integracao
            k = (v[j] * math.gamma(self.x1) * math.gamma(self.x2) *
                     math.gamma(self.x3) / math.gamma(self.x1 + self.x2 + self.x3))
            for i in c:
                if self.theta(i[0], i[1]) > k:
                    soma[j] += 1
        #somas = np.array(soma)
        return 1 - (soma / len(c))
    
#Definicao dos parametros  
#altere esses valores para testar o codigo



# media da dist normal utilizada
mean = np.array([0,0])
# definificao da matriz de covariancia utilizada
# dimensao 2 pois o terceiro valor eh um menos os outros dois
sigma = 0.02
cov = np.array([[sigma,0], [0,sigma]])
#Ponto inicial da cadeia
ponto_inicial = np.array([0.3, 0.3])
num = 100000
saltos = 10
n_cadeia_fria = num // 10



#calcula o tempo
now1 = datetime.now()

#gera a cadeia
mcmc = MCMC()
taxa = mcmc.run_MCMC(n_cadeia_fria, num, saltos, mean, cov, ponto_inicial)           
c = mcmc.cadeia

v = np.array([0,1,0.5,7,15])
#calcula os u(v)
lista = mcmc.u(c, v)
    
string = ""
for i in range(len(v)):
    string += f"U({v[i]}) = {lista[i]}\n"
print("As estimativas foram: ")
print(string)

print(f"A taxa de aceitacao foi de {taxa}%")
now2 = datetime.now()
print(f"Programa demorou {now2-now1} para rodar.\n")
print(f"Foram gerados {n_cadeia_fria + (num * saltos)} pontos sendo",
      f"{n_cadeia_fria} o tamanho da cadeia fria e {num * saltos} a",
      f"quantia gerada para se ter uma cadeia de tamanho {num} com",
      f"{saltos} saltos.\n")
print(f"A cadeia se iniciou no ponto {ponto_inicial} e variou a partir",
      "de uma normal multivariada com a seguinte distribuicao:")

string = f"  / |{mean[0]}| |{str(cov[0])[1:-1]}| \\\n"
string+= f"N \ |{mean[1]}|,|{str(cov[1])[1:-1]}| /"
print(string)











    
