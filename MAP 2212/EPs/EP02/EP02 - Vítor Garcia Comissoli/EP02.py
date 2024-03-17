#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np
from scipy.stats import beta

#Escreva seu nome e numero USP
INFO = {11810411:"Vítor Garcia Comissoli"}
A = 0.54018912  # A = 0.rg
B = 0.509920698  # B = 0.cpf

def f(x):
    """
    Esta funcao deve receber x e devolver f(x), como especifcado no enunciado
    Escreva o seu codigo nas proximas linhas
    """

    func = np.exp(-A*x)*np.cos(B*x) # Calcula o valor de f(x) para o x recebido na função e usando A e B como especificados no enunciado
    
    return func # Retorna o valor obtido




def crude(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo crude
    Escreva o seu codigo nas proximas linhas
    """
    
    soma = 0 # Inicialização da varável que vai obter a soma das n áreas
    
    n = 4502884 # N obitido pela aproximação assintótica a uma Normal(0,1)
    
    for i in range(n): # Repete n vezes
        
        x = random.uniform(0,1) # Coordenada X uniformemente aleatória entre 0 e 1
        valor = f(x) # Valor de F(x) para o X obtido acima
        soma += 1 * valor # Soma acrescenta a área do retângulo de altura f(x) e largura 1
        gamma = soma/n # É a estimativa para o valor da integral de f(x)
        
    return gamma # Retorna a estimativa




def hit_or_miss(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo hit or miss
    Escreva o seu codigo nas proximas linhas
    """
    
    dentro = 0 # Inicialização da variável que vai conter o número de pontos dentro da área de gamma
   
    n = 14853316 # N obitido pela aproximação assintótica a uma Normal(0,1)
   
    for i in range (n): # Repete n vezes
       
       x = random.uniform(0,1) # Coordenada X uniformemente aleatória entre 0 e 1
       y = random.uniform(0,1) # Coordenada Y uniformemente aleatória entre 0 e 1
       
       if y <= f(x): # Testa se a coordenada Y é menor que o valor de f(x), o que implica que Y está dentro da área de gamma
           dentro += 1 # Adiciona 1 ponto à variável "dentro"

       
    gamma = dentro/n # É a estimativa para o valor da integral de f(x)
   
    return gamma # Retorna a estimativa




def control_variate(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo control variate
    Escreva o seu codigo nas proximas linhas
    """
    
    soma = 0 # Inicialização da varável que vai obter a soma das n equações
    
    n = 100000 # N obitido pela aproximação assintótica a uma Normal(0,1)
    
    for i in range(n): # Repete n vezes
        
        x = random.uniform(0, 1) # Coordenada X uniformemente aleatória entre 0 e 1
        
        soma += (f(x) - h(x) + (3/4)) # Acrescenta o resultado de f(x) + h(x) + integral definida em [0,1] de h(x) (= 3/4) a variável soma
    
    gamma = soma/n # É a estimativa para o valor da integral de f(x)

    return gamma # Retorna a estimativa




def h(x): # Função que se assemelha muito ao comportamento de f(x) no intervalo [0,1]
    
    func = (- 0.5 * x) + 1 # Calcula o valor de g(x) para o x recebido na função
    
    return func # Retorna o valor obtido




def importance_sampling(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo importance sampling
    Escreva o seu codigo nas proximas linhas
    """

    soma = 0 # Inicialização da varável que vai obter a soma das n equações
    
    n = 3541924 # N obitido pela aproximação assintótica a uma Normal(0,1)
     
    for i in range(n): # Repete n vezes
        
        x = random.betavariate (1, 1.2) # Coordenada X aleatória entre 0 e 1 com fdp Beta(1,1.2)
        y = beta.pdf(x,1,1.2) # Uma g(x) que é uma fdp de Beta(1,1.2)
        
        soma += f(x)/y # Soma o valor de f(x) / g(x)

    gamma = soma/n # É a estimativa para o valor da integral de f(x)

    return gamma # Retorna a estimativa




def main():
    # Coloque seus testes aqui
                  
    print(crude())
    print(hit_or_miss())
    print(control_variate())
    print(importance_sampling())
    
if __name__ == "__main__":
    main()