#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
#Escreva seu nome e numero USP
INFO = {11810411:"Vítor Garcia Comissoli"}
def estima_pi(Seed = None):

    random.seed(Seed)
    #random.random() gera um numero com distribuicao uniforme em (0,1)
    """
    Esta funcao deve retornar a sua estimativa para o valor de PI
    Escreva o seu codigo nas proximas linhas
    """
    
    dentro = 0 # Quantidade de pontos "dentro" de 1/4 da circunferência
    
    n = 5121169 # N obitido pela aproximação assintótica a uma Normal(0,1)
    
    for i in range (n):
        
        x = random.uniform(0,1) # Coordenada X uniformemente aleatória entre 0 e 1
        y = random.uniform(0,1) # Coordenada Y uniformemente aleatória entre 0 e 1
        
        z = (x**2 + y**2)**(1/2) # Z é a hipotenusa do triângulo retângulo de catetos X e Y
        
        if z <= 1: #Testa se a hipotenusa obtida é menor que o raio da circunferência
            dentro += 1
        
    pi = 4*(dentro/n) # Estimativa de pi dado a proporcão de pontos dentro da circunferência inteira
    
    return pi #Retorne sua estimativa

def main():
    
    import numpy
    from time import process_time
    
    n = int(input('Digite n: '))
    
    t1 = process_time()
    
    erro = 0.0005 * 3 # Tomando Pi_chapéu como 3, é o erro de 0.05% de Pi_chapéu
    certo = 0 
    pi = numpy.pi
    soma = 0
    
    for j in range (n):
        x = (estima_pi())
        
        soma += x
        
        print(f"{j+1}-ésimo estimador: {x}")
        
        if x >= pi - erro and x <= pi + erro:
            certo += 1
    
    print("Média:", soma/n)
    print('certo/total:', certo/n)
    
    if certo/n < 0.95:
        print('teste falhou')
    else:
        print('teste funcionou')
    
    t2 = process_time()

    print("Tempo gasto pelo programa:", t2-t1)    
    
main()
