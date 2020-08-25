import pandas as pd
import Discrim.utileria as ut
from Discrim.Train import base_train
import os
import spacy
import nltk
import pickle as pickle
from sklearn.model_selection import train_test_split
import numpy as np
import dask.dataframe as dd

class Discapacidad(base_train.BaseTrain):
    
    def __init__(self):
        
        # Instanciamos la clase padre
        super().__init__()

        self.str_ruta_entrenamiento = '00_entrenamiento/tweets_modelo_capa2'
        self.str_fuente_clasificacion = 'tweets_entrenamiento_discapacidad_balance.csv'
        self.str_LocalFile = 'data/tweets/' + self.str_fuente_clasificacion
        self.str_nombrePickle = 'modelo_capa2_discapacidad_prueba.p'
        self.str_ruta_s3_modelos = '01_modelos/capa2/discapacidad'
        self.str_modelo_pickle_s3 = self.str_ruta_s3_modelos+'/'+self.str_nombrePickle
        
        ############################### Parametrización de modelos para el magic loop ##########################
        
        self.npDictHiperParam = np.array([])
        
        # Parametrización para Árboles
        dictHyperParams = {'max_depth': [4,7],  # 
                           'min_samples_split': [4,16],  # 
                           'min_samples_leaf': [3,7],  # 
                           'max_features': ['sqrt','log2']  # 
                           }
        self.npDictHiperParam = np.append(self.npDictHiperParam, dictHyperParams)

        # Parametrización para Bosques
        dictHyperParams = {'n_estimators': [50],  # Se redujo a 50
                           'max_depth': [4,7],  # 
                           'max_features': ['sqrt','log2'],
                           'min_samples_split': [4,16],
                           'min_samples_leaf': [3,7]
                           }
        self.npDictHiperParam = np.append(self.npDictHiperParam, dictHyperParams)

        # Parametrización para XGBoost
        dictHyperParams = {'learning_rate': [0.1,0.75], #0.25
                           'n_estimators': [100],  # Se redujo a 50
                           'min_samples_split': [4,16],
                           'min_samples_leaf': [3],
                   'max_depth': [3,6,7],
                           'max_features': ['sqrt'] #listo amigo
                           }
        self.npDictHiperParam = np.append(self.npDictHiperParam, dictHyperParams)

        # Se crean los modelos de clasificaión que se emplearán (en el mismo orden que los diccionarios)
        self.npNombreModelos = np.array([])
        self.npNombreModelos = np.append(self.npNombreModelos, 'DECTREE')
        self.npNombreModelos = np.append(self.npNombreModelos, 'RANDOMF')
        self.npNombreModelos = np.append(self.npNombreModelos, 'XGBOOST')
        
        self.nbv_cross_validation = 5
        self.str_metric = 'f1'
        
        return