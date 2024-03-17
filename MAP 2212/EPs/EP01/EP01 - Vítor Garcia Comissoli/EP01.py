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
