# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import dirichlet as dr

#Escreva seus nomes e numeros USP
INFO = {11810411:"Vítor Garcia Comissoli", 11288131:"Ayrton Amaral Alves Vítor"}

media_esqt = np.random.multivariate_normal(np.zeros(2),np.identity(2) * 4)
cov_esqt = np.identity(2) * 4

def amostra_MCMC(x,y,n):
    """
    Funcao que recebe valores pros vetores x e y, o tamanho n da amostra, 
    gera uma amostra de tamanho n a partir do metodo de monte carlo via 
    cadeias de markov, onde cada elemento da amostra tem tamanho 3 (vetor),
    e retorna uma lista de tamanho n com os potenciais de cada ponto obtido,
    onde cada elemento tem tamanho 1 (escalar).
    
    Nao utilize a fuancao densidade de probabilidade, apenas a funcao potencial!
    """
    amostras = np.zeros((n + 1, 2))
    densidades = np.ones(n + 1)
    amostras[0] = np.array([.5182, .1626]) # média esquentada
    cov_esqt = np.identity(2) * 2
    n_aceitas = 0
    xarr = np.array(x)
    yarr = np.array(y)
    densidades[0] = potencial_dirichlet(np.concatenate((amostras[n_aceitas], [1 - amostras[n_aceitas].sum()])), xarr + yarr - 1)

    while n_aceitas < n:
        amostra_normal = np.random.multivariate_normal(amostras[0], cov_esqt)

        novo_pot = potencial_dirichlet(np.concatenate((amostra_normal, [1 - amostra_normal.sum()])), xarr + yarr - 1)

        # razao de potenciais para aceitacao
        prob = min(1, (novo_pot / densidades[n_aceitas]))

        if np.random.rand() < prob:
            n_aceitas += 1
            amostras[n_aceitas] = amostra_normal
            densidades[n_aceitas] = novo_pot
        
    amostra_de_potenciais = densidades[1:]
    return amostra_de_potenciais # Exemplo do formato = [0.04867, 0.00236, 0.00014 ... ]

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
        Caso tenha feito no EP04, pode copiar o codigo aqui.
        """
        self.vetor_x = x #formato: [0,0,0] - List cujo len(x) = 3
        self.vetor_y = y #formato: [0,0,0] - List cujo len(y) = 3
        #Continue o codigo conforme achar necessario
        
        array_x = np.array(x) # transforma a lista x em um array
        array_y = np.array(y) # transforma a lista y em um array
        self.alpha =  array_x + array_y # concatena os arrays
       
        self.n = 28000 # N decidido para um erro < 0.0005
        self.k = self.n // 2 # número de bins
       
        f_theta = amostra_MCMC(x,y, self.n) # chama a função amostra_MCMC
       
        self.v_hat = gera_v(self.k, f_theta) # chama a função gera_v

    def U(self,v):
        """
        Este metodo recebe um valor para v e, a partir dele, retorna U(v|x,y) a partir dos 
        vetores x e y inicializados anteriormente
        Caso tenha feito no EP04, pode copiar o codigo aqui.
        """
        # Continue o codigo conforme achar necessario
        
        dentro = np.where(self.v_hat <= v, 1, 0) # lista com 1s para valores que condizem com a condição e 0 c.c.
        u = np.sum(dentro) / self.k # soma de valores que condizem com a condição / número total de bins
       
        return u # retorna a estimativa para u

    ############################################################################
    # Escreva aqui embaixo qualquer outro metodo ou funcao que voce queira utilizar no
    # exercício. Pedimos que mantenha o nome dos metodos ja definidos acima, 
    # os inputs do __init__() e do U() precisam ser mantidos iguais, assim como
    # os outputs.
    # ela implemente a estimativa U(v). Esse formato utilizado e demonstrado no
    # main sera utilizado pelo corretor automativo.
    # 
    # Exemplo de funcionamento do corretor:
    # 
    #           from EP04 import estimador
    #           estimativa_do_aluno = estimador([1,2,3],[4,5,6])
    #           if abs(estimativa_do_aluno.U(7) - W(7)) <= 0.0005:
    #               print("Parabens, mais 5 na nota") 
    #           if abs(estimativa_do_aluno.U(0.2) - W(0.2)) <= 0.0005:
    #               print("Parabens, mais 5 na nota")
    # 
    ############################################################################

    # Dica: Tente implementar o Estimador() de tal forma que a inicializacao seja
    # demorada, mas a chamada do metodo U(v) seja rapida. Ou seja, tente implementar
    # o maximo possivel do exercicio sem utilizar o valor de v. Desta forma, voce
    # pode acelerar o calculo de estimativas U(v) para diferentes valores de v 
    # sem precisar repetir todo o procedimento do exercicio para cada novo v.

def potencial_dirichlet(x, alfa):
    if not 0 <= x.sum() <= 1 or \
        (x < 0).any() or (x > 1).any() != 0:
        return 0
    return (x ** alfa).prod()
    # return dr.pdf(x, alfa)

#----------------------------------------------------------------------------------------------------    

def gera_v(k, f_theta):
    dim_theta = f_theta.shape[0]
    extra = k - dim_theta % k                       # número de zeros a adicionar ao array se dimenção de theta nao e divisível por k
    if extra == k:
        extra = 0
    ordenado_completo = np.zeros(dim_theta + extra) # array de tamanho múltiplo de k
    
    ordenado = np.sort(f_theta)                     # ordena os valores da f(theta)
    ordenado_completo[:dim_theta] = ordenado        # último bin possivelmente tem zeros adicionais, mas queremos apenas o max
    bins = np.array(np.split(ordenado_completo, k)) # divide os dados em k bins
    
    return bins.max(axis=1)

def main():
    #Coloque seus testes aqui
    print("Segue um exemplo de funcionamento:")
    print("Criando o objeto")
    estimativa = Estimador([4,6,4],[1,2,3])
    print("Implementando o valor para v")
    print(f"Temos que U({0}) = {estimativa.U(0)}")
    print(f"Para um novo valor de v, temos que U({1}) = {estimativa.U(1)}")
    print(f"Para um novo valor de v, temos que U({.5}) = {estimativa.U(.5)}")
    print(f"Para um novo valor de v, temos que U({15}) = {estimativa.U(15)}")
    print(f"Para um novo valor de v, temos que U({500}) = {estimativa.U(500)}")
    print()
    print(f"Os valores dos vetores utilizados sao: {estimativa.vetor_x,estimativa.vetor_y}")
    print("Este exemmplo foi feito para demonstrar o funcionamento esperado do objeto")

if __name__ == "__main__":
    main()
