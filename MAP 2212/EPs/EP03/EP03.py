#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np
from scipy.stats import beta
import chaospy as ch

#Escreva seu nome e numero USP
INFO = {11801411:"Vítor Garcia Comissoli"}
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
    
    n = 700000 # N obtido experimentalmente para que IC seja [+- gamma_chapeu * 0.005] com alpha 0.95
    
    x_array = (ch.Uniform(0, 1)).sample(n) # Array de coordenadas X uniformemente quasi-random entre 0 e 1  
        
    valor = f(x_array) # Array com os valores de F(x) para o X obtido acima
    soma = sum(1 * valor) # Soma as áreas do retângulo de altura f(x) e largura 1
    gamma = soma/n # É a estimativa para o valor da integral de f(x)
        
    return gamma # Retorna a estimativa


def hit_or_miss(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo hit or miss
    Escreva o seu codigo nas proximas linhas
    """
   
    n = 6000000 # N obtido experimentalmente para que IC seja [+- gamma_chapeu * 0.005] com alpha 0.95
    
    x_array = (ch.Uniform(0, 1)).sample(n) # Array de coordenadas X uniformemente quasi-random entre 0 e 1  
    y_array = (ch.Uniform(0, 1)).sample(n) # Array de coordenadas Y uniformemente quasi-random entre 0 e 1  
       
    dentro = sum(y_array <= f(x_array)) # Testa e soma as coordenadas Y que são menores iguais aos valores de f(x), o que implica que Y está dentro da área de gamma
       
    gamma = dentro/n # É a estimativa para o valor da integral de f(x)
   
    return gamma # Retorna a estimativa


def control_variate(Seed = None):
    random.seed(Seed)
    """
    Esta funcao deve retornar a sua estimativa para o valor da integral de f(x)
    usando o metodo control variate
    Escreva o seu codigo nas proximas linhas
    """
    
    n = 750 # N obtido experimentalmente para que IC seja [+- gamma_chapeu * 0.005] com alpha 0.95
    
    x_array = (ch.Uniform(0, 1)).sample(n) # Array de coordenadas X uniformemente quasi-random entre 0 e 1  
        
    soma = sum(f(x_array) - h(x_array) + (3/4)) # Soma todos os resultados de f(x) + h(x) + integral definida em [0,1] de h(x) (= 3/4)
    
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
    
    n = 150000 # N obtido experimentalmente para que IC seja [+- gamma_chapeu * 0.005] com alpha 0.95
    
    x_array = (ch.Beta(1, 1.2)).sample(n) # Array de coordenadas X quasi-random entre 0 e 1 com fdp Beta(1,1.2)
        
    y_array = beta.pdf(x_array,1,1.2) # Um Array de g(x) que é uma fdp de Beta(1,1.2)
    
    soma = sum(f(x_array)/y_array) # Soma o valor de todas as f(x) / g(x)
    
    gamma = soma/n # É a estimativa para o valor da integral de f(x)

    return gamma # Retorna a estimativa


def main():
    #Coloque seus testes aqui
    print(crude())
    print(hit_or_miss())
    print(control_variate())
    print(importance_sampling())
    

if __name__ == "__main__":
    main()