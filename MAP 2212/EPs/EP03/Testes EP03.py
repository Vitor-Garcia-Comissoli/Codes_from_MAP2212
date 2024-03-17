# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:38:23 2022

@author: Vítor Garcia Comissoli
"""

import EP03 as ep

def main():
    # Coloque seus testes aqui
    
    from time import process_time
    
    n = int(input('Digite n: '))
    
    metodo = str(input('Digite o método: '))
    if metodo != 'crude' and metodo != 'hit or miss' and metodo != 'control variate' and metodo != 'importance sampling' and metodo != 'all':
        print("ERRO: Método inválido")
        return 
    
    print('\n')
    
    gamma_hat = 0.74391 # Proviniente da função control_variates() para um n = 1000000
    erro = 0.0005 * gamma_hat # Tomando gamma_chapéu como 0.74391, é o erro de 0.05% de gamma_chapéu
    
    if metodo == 'crude' or metodo == 'all':
    
        certo = 0 
        soma = 0
    
        t1 = process_time()
    
        for j in range (n):
            x = (ep.crude())
            
            soma += x
        
            print(f"{j+1}-ésimo estimador: {x}")
        
            if x >= gamma_hat - erro and x <= gamma_hat + erro:
                certo += 1
    
        print("Média:", soma/n)
        print('certo/total:', certo/n)
    
        if certo/n < 0.95:
            print('teste falhou')
        else:
            print('teste funcionou')
    
        t2 = process_time()

        print("Tempo gasto pelo programa:", t2-t1,"\n")
    
    #-----------------------------------------------------
    
    if metodo == 'hit or miss' or metodo == 'all':
    
        certo = 0
        soma = 0
        
        t1 = process_time()
         
        for j in range (n):
             x = (ep.hit_or_miss())
             
             soma += x
             
             print(f"{j+1}-ésimo estimador: {x}")
             
             if x >= gamma_hat - erro and x <= gamma_hat + erro:
                 certo += 1
         
        print("Média:", soma/n)
        print('certo/total:', certo/n)
         
        if certo/n < 0.95:
             print('teste falhou')
        else:
             print('teste funcionou')
         
        t2 = process_time()
    
        print("Tempo gasto pelo programa:", t2-t1,"\n") 
    
    #-----------------------------------------------------
    
    if metodo == 'control variate' or metodo == 'all':
    
        certo = 0
        soma = 0
     
        t1 = process_time()
        
        for j in range (n):
            x = (ep.control_variate())
            
            soma += x
            
            print(f"{j+1}-ésimo estimador: {x}")
            
            if x >= gamma_hat - erro and x <= gamma_hat + erro:
                certo += 1
        
        print("Média:", soma/n)
        print('certo/total:', certo/n)
        
        if certo/n < 0.95:
            print('teste falhou')
        else:
            print('teste funcionou')
        
        t2 = process_time()
    
        print("Tempo gasto pelo programa:", t2-t1,"\n")

    #-----------------------------------------------------
    
    if metodo == 'importance sampling' or metodo == 'all':
    
        certo = 0
        soma = 0
        
        t1 = process_time()
         
        for j in range (n):
             x = (ep.importance_sampling())
             
             soma += x
             
             print(f"{j+1}-ésimo estimador: {x}")
             
             if x >= gamma_hat - erro and x <= gamma_hat + erro:
                 certo += 1
         
        print("Média:", soma/n)
        print('certo/total:', certo/n)
         
        if certo/n < 0.95:
             print('teste falhou')
        else:
             print('teste funcionou')
         
        t2 = process_time()
        
        print("Tempo gasto pelo programa:", t2-t1,"\n")

main()