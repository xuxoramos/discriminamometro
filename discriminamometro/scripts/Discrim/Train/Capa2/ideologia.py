import pandas as pd
import Discrim.utileria as ut
import Discrim.magic_loop as mgl
import os
import spacy
import nltk
import pickle as pickle
from sklearn.model_selection import train_test_split
import numpy as np

class Ideologia():
    
    def __init__(self):
        
        self.obj_utileria = ut.Utileria()
        self.str_ruta_entrenamiento = '00_entrenamiento/tweets_modelo_capa2'
        self.str_fuente_clasificacion = 'tweets_entrenamiento_ideologia.csv'
        self.str_LocalFile = 'data/tweets/' + self.str_fuente_clasificacion
        self.str_nombrePickle = 'modelo_capa2_ideologia.p'
        self.str_ruta_s3_modelos = '01_modelos/capa2/ideologia'
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
        dictHyperParams = {'learning_rate': [0.1,0.25, 0.75],
                           'n_estimators': [50,100,150],  # Se redujo a 50
                           'min_samples_split': [4,16],
                           'min_samples_leaf': [3,7],
                           'max_depth': [3,4,5,6,7,10,15],
                           'max_features': ['sqrt','log2']
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

    def cargar_modelo_embeddings(self):
        
        self.nlp = spacy.load('./data/')
        
        return
    
    def descargar_tweets_entrenamiento(self):
        
        s3 = self.obj_utileria.crear_conexion_s3()
        
        with open(self.str_LocalFile, 'wb') as f:
            s3.download_fileobj(self.obj_utileria.str_NombreBucket,  self.str_ruta_entrenamiento+'/'+self.str_fuente_clasificacion, f)
        
        return
    
    def transformar_dataset(self):
        
        # self.pd_fuente = pd.read_csv('tmp_fuente_embeddings.csv', lineterminator='\n') 
        self.pd_fuente = pd.read_csv(self.str_LocalFile, lineterminator='\n') 
        
        self.obj_utileria.cargar_stop_words()
        nltk.download('punkt')
                
        self.pd_fuente = self.obj_utileria.formatear_dataframe(self.pd_fuente)
        
        
        return
    
    def train(self):
        
        self.train, self.test = train_test_split(self.pd_fuente, test_size=0.2,random_state = 202008)
        
        self.cargar_modelo_embeddings()
        npEmbeddings = self.generar_embeddings(self.train)
        
        obj_mgl = mgl.MagicLoop()
        
        # obj_mgl.train(npEmbeddings, self.train.label, )
        
        X_train = pd.DataFrame(npEmbeddings)
        Y_train = pd.DataFrame(self.train.label)
        arrModelos = obj_mgl.prep_modelos(self.npNombreModelos)

        # #Se corre el magic loop para realizar las predicciones con los parámetros previamente establecidos
        self.best_model, npGridSearchCv = obj_mgl.correr_magic_loop(arrModelos,
                                            self.npDictHiperParam,
                                            X_train,
                                            Y_train,
                                            self.nbv_cross_validation,
                                            self.str_metric)    
    
    def generar_embeddings(self, fuente):
        
        npEmbeddings = np.empty([0, 300])

        for texto in fuente['full_text']:

            #print(texto)

            # process a sentence using the model
            doc = self.nlp(texto)

            # print(doc.vector.shape)
            if doc.vector.shape[0]==300:
                npEmbeddings = np.append(npEmbeddings, [doc.vector], axis = 0)
            else:
                npAux = np.empty([1, 300])
                npEmbeddings = np.append(npEmbeddings, npAux, axis = 0)
        
        return npEmbeddings 
    
    def crear_pickle(self):
    
        pickleFile = open(self.str_nombrePickle, 'wb')
        pickle.dump(self.best_model, pickleFile)
        pickleFile.close()
        
        return
        
    def mandar_pickle_s3(self):

        # Una vez generado el archivo, lo envíamos a S3
        
        cnx_S3 = self.obj_utileria.crear_conexion_s3()

        # Mandamos el archivo descargado a S3
        try:
            self.obj_utileria.mandar_archivo_s3(cnx_S3, self.obj_utileria.str_NombreBucket, self.str_ruta_s3_modelos+'/', self.str_nombrePickle)
        except Exception as e:
            with open('Error_mandar_pickle_s3.txt', 'w') as file:
                file.write(str(e))
            raise

        return