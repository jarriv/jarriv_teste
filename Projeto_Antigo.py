#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd

from sklearn.utils import all_estimators
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore')

global classif_lista_pontos
classif_lista_pontos = [[],[],[],[]]



############################################################################################

class Classe_Correcao:
    
    def impresssao_teste(self):
        print("Teste do Jarriv Reginaldo")
        
    
    def impressao_teste_2(self):
        self.impresssao_teste()

    def importar_pontos(self):
        
        for i in range(301)[1:]:
   
            tabela_pontos_a = pd.read_csv("./ASD/ASD_scanpath_"+str(i)+".txt", sep=",") # Leitura das coordenadas, com separação por vírgula
            tabela_pontos_a.columns = tabela_pontos_a.columns.str.replace(' ','') # Retira o espaço do título das colunas
            tabela_pontos_a
            
            X_a = tabela_pontos_a.iloc[:,1:3].values # Seleciona os valores de X e y
            y_a = np.ones((X_a.shape[0]), dtype=int)
            
            tabela_pontos_b = pd.read_csv("./TD/TD_scanpath_"+str(i)+".txt", sep=",") # Leitura das coordenadas, com separação por vírgula
            tabela_pontos_b.columns = tabela_pontos_b.columns.str.replace(' ','') # Retira o espaço do título das colunas
            tabela_pontos_b
            
            X_b = tabela_pontos_b.iloc[:,1:3].values # Seleciona os valores de X e y
            y_b = np.zeros((X_b.shape[0]), dtype=int)
            
            X = np.concatenate((X_a, X_b), axis=0)
            y = np.concatenate((y_a, y_b), axis=0)
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.4, random_state=50)
            
            classif_lista_pontos[0].append(X_train)
            classif_lista_pontos[1].append(X_test)
            classif_lista_pontos[2].append(y_train)
            classif_lista_pontos[3].append(y_test)
            
        
        #return X_train, X_test, y_train, y_test
    
    def lista_classificadores(self):
        global classif_nomes,classif_lista
        
        estimators = all_estimators(type_filter='classifier') # Todos os classificadores do Sklearn
        
        classif_nomes = [] # Lista que armazenará os nomes dos classificadores válidos
        classif_lista = [] # Lista que armazerará os classificadores válidos
        
        for name, ClassifierClass in estimators:
            #print('Appending', name)
            try:
                clf = ClassifierClass()
                classif_lista.append(clf)
                classif_nomes.append(name)
            except:
                #print('Unable to import', name)
                #print(e)
                pass
                
        #return classif_nomes,classif_lista
    
    def importar_classificadores(self):
        
        self.lista_classificadores()
        
        planilha = pd.read_csv("./classif_imagens_cross_tamanho_imagem.txt", sep=",")
        
        global classif_ranking
        classif_ranking = np.empty([300, 6], dtype=object)

        for i in range(300):
          classif_ranking[i][0] = planilha.iloc[i][0] # Importa o número da imagem
          classif_ranking[i][1] = planilha.iloc[i][1] # Importa o percentual de acerto
          classif_ranking[i][2] = planilha.iloc[i][2] # Importa o nome do classificador
          classif_ranking[i][3] = classif_lista[classif_nomes.index(planilha.iloc[i][2])] # Importa as características de uso do classificador
          classif_ranking[i][4] = planilha.iloc[i][3] # Importa a altura da imagem
          classif_ranking[i][5] = planilha.iloc[i][4] # Importa a largura da imagem 

    def importar_teste(self,tabela_teste):
        
        global planilha_teste
        global planilha_teste
        
        planilha_teste = pd.read_csv(tabela_teste, sep=" ")
        return planilha_teste
    
    
    def predicao(self):
        resultado_predicao = ""
        #print(Foto,x,y,Classificador)
        
        for i in planilha_teste['Foto'].unique(): 
            
            pontos_autismo = 0
            pontos_nao_autismo = 0
            pontos_total = 0
            
            tabela_selecao = planilha_teste.loc[planilha_teste.Foto==i]
            
            for j in range(len(tabela_selecao)):
                
                pontos_total+=1

                Foto = tabela_selecao.iloc[j]['Foto'] # Número da imagem
                X = tabela_selecao.iloc[j]['x'] # Coordenada x
                y = tabela_selecao.iloc[j]['y'] # Coordenada y
                Larg_Imagem = tabela_selecao.iloc[j]['Larg_Imagem'] # Largura da imagem apresentada na página do teste
                Alt_Imagem = tabela_selecao.iloc[j]['Alt_Imagem']  # Altura da imagem apresentada na página do teste
                Larg_Tela = tabela_selecao.iloc[j]['Larg_Tela'] # Largura da página aonde a imagem foi apresentada
                Alt_Tela = tabela_selecao.iloc[j]['Alt_Tela'] # Altura da página aonde a imagem foi apresentada
                Dist_Larg = tabela_selecao.iloc[j]['Dist_Larg'] # Distância entre a borda esquerda e a lateral esquerda da imagem
                Dist_Alt = tabela_selecao.iloc[j]['Dist_Alt'] # Distância entre a borda supoerior e o topo da imagem
                Classificador = classif_ranking[Foto-1][3] # Detalhes do melhor classificador para a imagem
                X_train_temp = classif_lista_pontos[0][Foto-1] # Pontos X de treino
                y_train_temp = classif_lista_pontos[2][Foto-1] # Pontos y de treino
            
                alt_imagem = classif_ranking[Foto-1][4] # Altura real da imagem
                larg_imagem = classif_ranking[Foto-1][5] # Largura real da imagem
        
        
        
        ##########################################################################
        
                model = Classificador
                model.fit(X_train_temp, y_train_temp) # Ajustar
                
                ponto_x = ((X - Dist_Larg)/Larg_Imagem)*larg_imagem
                ponto_y = ((y - Dist_Alt)/Alt_Imagem)*alt_imagem
                center_coordinates = (int(ponto_x),int(ponto_y))
                
                predicao = model.predict([[center_coordinates[0],center_coordinates[1]]])
        
        ###############################################################################
        
        
                if (predicao==0):
                    pontos_nao_autismo+=1
                else:
                    pontos_autismo+=1
            
                linha = "Figura = " + str(Foto) +" | x = " + str(X) + " | y = " +  str(y) + " | Predição = " + str(predicao)
                resultado_predicao = resultado_predicao+linha+"\n"
                
            linha = "Pontos Não Autista: " + str(pontos_nao_autismo)
            resultado_predicao = resultado_predicao+linha+"\n"
            
            linha = "Pontos Autista: " + str(pontos_autismo)
            resultado_predicao = resultado_predicao+linha+"\n"
            
            linha = "Pontos Total: " + str(pontos_total)
            resultado_predicao = resultado_predicao+linha+"\n\n"
                
                #print(linha)
        
        return resultado_predicao
    
    
    
    def acao_botao(self,arquivo):
        
        self.importar_pontos()
        self.importar_classificadores()
        self.importar_teste(arquivo)
        
        resultado = self.predicao()
        
        return resultado
