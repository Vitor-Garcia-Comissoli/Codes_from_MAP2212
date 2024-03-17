#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.stats import dirichlet as dr

#Escreva seus nomes e numeros USP
INFO = {11810411:"Vítor Garcia Comissoli", 11288131:"Ayrton Amaral Alves Vítor"}

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
        self.vetor_x = x #formato: [0,0,0] - List cujo len(x) = 3
        self.vetor_y = y #formato: [0,0,0] - List cujo len(y) = 3
        #Continue o codigo conforme achar necessario.
        
        array_x = np.array(x) # transforma a lista x em um array
        array_y = np.array(y) # transforma a lista y em um array
        alpha = array_x + array_y # concatena os arrays
        
        n = 36000000 # N decidido para um erro < 0.0005
        self.k = n/2 # número de bins
        
        theta = dirichlet(alpha, n) # chama a função dirichlet
        f_theta = f_dirichlet(alpha, theta) # chama a função f_dirichlet
        
        self.v_hat = gera_v(self.k, f_theta) # chama a função gera_v

    def U(self,v):
        """
        Este metodo recebe um valor para v e, a partir dele, retorna U(v|x,y) a partir dos 
        vetores x e y inicializados anteriormente
        """
        # Continue o codigo conforme achar necessario
        
        k = self.k # pega o valor designado no __init__ da  classe para uma variável k
        v_hat = self.v_hat # pega o valor designado no __init__ da  classe para uma variável v_hat
        
        dentro = np.where(v_hat <= v, 1, 0) # lista com 1s para valores que condizem com a condição e 0 c.c.
        u = np.sum(dentro)/k # soma de valores que condizem com a condição / número total de bins
        
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

def dirichlet(alpha, n):

    dist = np.random.dirichlet(alpha, n) # gera pontos com dist dirichlet
    return dist # retorna os pontos

def f_dirichlet(alpha, theta):
    
    return dr.pdf(theta.T, alpha) # retorna um array com o valor da FDP da dirichlet

def gera_v(k, f_theta):
    
    dim_theta = f_theta.shape[0] # dimensão de theta
    
    extra = k - dim_theta % k # número de zeros a adicionar ao array se dimenção de theta não é divisivel por k
    if extra == k:
        extra = 0
        
    ordenado_completo = np.zeros(dim_theta + extra) # array de tamanho múltiplo de k
    
    ordenado = np.sort(f_theta) # ordena os valores da f(theta)
    ordenado_completo[:dim_theta] = ordenado # último bin possivelmente tem zeros adicionais, mas queremos apenas o max
    bins = np.array(np.split(ordenado_completo, k)) # divide os dados em k bins
    
    return bins.max(axis=1) # retorna o max de cada bin

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
