#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import numpy as np
import scipy.stats as stats
import scipy.optimize as opt
from scipy.stats import chi2 as qq

#Escreva seus nomes e numeros USP
INFO = {11810411:"Vítor Garcia Comissoli", 11288131:"Ayrton Amaral Alves Vítor"}

PONTOS = np.array([[1, 20 - 1 - 2, 2],
       [1, 20 - 1 - 3, 3],
       [1, 20 - 1 - 4, 4],
       [1, 20 - 1 - 5, 5],
       [1, 20 - 1 - 6, 6],
       [1, 20 - 1 - 7, 7],
       [1, 20 - 1 - 8, 8],
       [1, 20 - 1 - 9, 9],
       [1, 20 - 1 - 10, 10],
       [1, 20 - 1 - 11, 11],
       [1, 20 - 1 - 12, 12],
       [1, 20 - 1 - 13, 13],
       [1, 20 - 1 - 14, 14],
       [1, 20 - 1 - 15, 15],
       [1, 20 - 1 - 16, 16],
       [1, 20 - 1 - 17, 17],
       [1, 20 - 1 - 18, 18],
       [5, 20 - 5 - 0, 0],
       [5, 20 - 5 - 1, 1],
       [5, 20 - 5 - 2, 2],
       [5, 20 - 5 - 3, 3],
       [5, 20 - 5 - 4, 4],
       [5, 20 - 5 - 5, 5],
       [5, 20 - 5 - 6, 6],
       [5, 20 - 5 - 7, 7],
       [5, 20 - 5 - 8, 8],
       [5, 20 - 5 - 9, 9],
       [5, 20 - 5 - 10, 10],
       [9, 20 - 9 - 0, 0],
       [9, 20 - 9 - 1, 1],
       [9, 20 - 9 - 2, 2],
       [9, 20 - 9 - 3, 3],
       [9, 20 - 9 - 4, 4],
       [9, 20 - 9 - 5, 5],
       [9, 20 - 9 - 6, 6],
       [9, 20 - 9 - 7, 7]])

class Estimador:
    """
    Classe para criar o objeto, ele recebe valores para os vetores x e y.
    Os metodos definidos abaixo serao utilizadas por um corretor automatico. Portanto,
    precisa manter os outputs e inputs dos 2 metodos abaixo. 
    """
    def __init__(self,x,y):
        """
        Inicializador do objeto. Este metodo recebe 
        valores pros vetores x e y em formato de lista 
        e implementa no objeto. 
        """
        
        n = 70000 # N decidido para um erro < 0.0005
        self.rv = MCMC(n, x, y)


    def U(self, v):
        """
        Este metodo recebe um valor para v e, a partir dele, retorna U(v|x,y) a partir dos 
        vetores x e y inicializados anteriormente
        """
        # Continue o codigo conforme achar necessario
        return self.rv.u(v)

class MCMC:
    def __init__(self, num = 100000, x = np.array([4,6,4]), y = np.array([1,2,3]),
                 saltos = 10, n_cadeia_fria = 3000):
        self.num = num   #numero de pontos
        self.x = x  #vetor x
        self.y = y  #vetor y
        self.saltos = saltos
        self.n_cadeia_fria = n_cadeia_fria
        self.x1 = x[0] + y[0]
        self.x2 = x[1] + y[1]
        self.x3 = x[2] + y[2]  # vetor x+y
        self.cadeia = np.array([])
        mean = np.array([0,0])
        sigma = 0.02
        cov = np.array([[sigma,0], [0,sigma]])
        ponto_inicial = np.array([0.3, 0.3])
        self.run_MCMC(n_cadeia_fria, num, saltos, mean, cov, ponto_inicial)

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
        
        cadeia_final = np.zeros((tamanho_da_cadeia, 2))
        for i in range(tamanho_da_cadeia):
            cadeia_final[i] = cadeia[saltos * i]
        self.cadeia = cadeia_final
        return taxa

    def u(self, v):
        # calculo de u a partir da cadeia e de um valor v de corte
        soma = 0            
        k = (v * math.gamma(self.x1) * math.gamma(self.x2) *
                 math.gamma(self.x3) / math.gamma(self.x1 + self.x2 + self.x3))
        for i in self.cadeia:
            if self.theta(i[0], i[1]) > k:
                soma += 1
        return 1 - (soma / self.cadeia.shape[0])


# maximiza densidade sob hipótese nula
def g(w, param):
    theta = (w, 2 * (np.sqrt(w) - w), (1 - np.sqrt(w)) ** 2)
    return - stats.dirichlet(param).pdf(theta)


def hyp_test(x,y):
    param = np.array([x[0] + y[0], x[1] + y[1], x[2] + y[2]])
    
    if param[0] == 0 or param[1] == 0 or param[2] == 0:
        return f"x1={x[0]}, x3={x[2]}, Y= {y[1]}, H=Indeciso," + \
                    "  θ*= {[0,0,0]}, ev(H|X)=0.000000 e sev(H|X)=0.000000"
    
    est = Estimador(x,y)
    start = np.random.dirichlet(param)[0]
    w_objeto = opt.minimize(g, start, param, bounds=[(0, 1)])
    
    w = w_objeto.x[0] #ponto minimo
    teta_est = (w, 2 * (np.sqrt(w) - w), (1 - np.sqrt(w)) ** 2) 
    
    ev = est.U(stats.dirichlet(param).pdf(teta_est))

    t = 2
    h = 1
    
    sev = 1 - stats.chi2.cdf(stats.chi2.ppf(1 - ev, t), t - h)
    
    alfa_s = 0.95 #aceitacao
    alfa_i = 0.90 #rejeicao
    if ev >= alfa_s and sev >= alfa_s:
        res = "Aceita"
    elif ev < alfa_i and sev < alfa_i:
        res = "Rejeita"
    else:
        res = "Indeciso"

    print(f"x1={x[0]}, x3={x[2]}, Y={y[1]}, H={res},  θ*={teta_est}, ev(H|X)={ev}, sev(H|X)={sev}")
    

def main():
    for y in ([0, 0, 0], [1, 1, 1]):
        for x in PONTOS:
            hyp_test(x, y)
            
if __name__ == "__main__":
    main()
