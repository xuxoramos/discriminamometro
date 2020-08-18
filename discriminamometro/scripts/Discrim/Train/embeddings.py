import pandas as pd
import Discrim.utileria as ut
import dask.dataframe as dd
import os
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
from nltk import word_tokenize
import nltk

class Embeddings():
    
    def __init__(self):
        
        self.obj_util = ut.Utileria()
        self.str_ruta_entrenamiento = '00_entrenamiento/embeddings'
        self.str_fuente_embeddings = 'tweets_agosto_prueba.csv'
        self.str_ArchivoLocalEmbeddings = './data/word2vec_Embeddings.txt'
        self.nbr_cpu = os.cpu_count() 
        
        return
    
    def descargar_archivo_fuente(self):
        
        s3 = self.obj_util.crear_conexion_s3()
        
        str_LocalFile = 'tmp_fuente_embeddings.csv'
        with open(str_LocalFile, 'wb') as f:
            s3.download_fileobj(self.obj_util.str_NombreBucket,  self.str_ruta_entrenamiento+'/'+self.str_fuente_embeddings, f)

        return
    
    def transformar_dataset(self):
        
        self.pd_fuente = pd.read_csv('tmp_fuente_embeddings.csv', lineterminator='\n') 
        
        self.obj_util.cargar_stop_words()
        nltk.download('punkt')
        
        ddf = dd.from_pandas(self.pd_fuente, npartitions=self.nbr_cpu)        
        self.pd_fuente = ddf.map_partitions(self.obj_util.limpiar_dataframe, meta=ddf).compute()
        
        ddf = dd.from_pandas(self.pd_fuente, npartitions=self.nbr_cpu)
        self.pd_fuente = ddf.map_partitions(self.obj_util.quitar_stop_words_dataframe, meta=ddf).compute()
        
        self.pd_fuente = self.pd_fuente["full_text"]
        self.pd_fuente = self.pd_fuente.apply(word_tokenize)     
        self.pd_fuente.to_list()
        
        return
    
    def generar_embeddings(self):
        
        path = get_tmpfile("./data/word2vec_Embeddings.model")

        model = Word2Vec(self.pd_fuente, size=300, window=5, min_count=1, workers=self.nbr_cpu)
        model.wv.save_word2vec_format(self.str_ArchivoLocalEmbeddings)
        
        return
    
    def enviar_embeddings_s3(self):
        
        cnx_S3 = self.obj_util.crear_conexion_s3()


        # Mandamos el archivo descargado a S3
        try:
            self.obj_util.mandar_archivo_s3(cnx_S3, self.obj_util.str_NombreBucket, self.str_ruta_entrenamiento+'/', self.str_ArchivoLocalEmbeddings)
        except Exception as e:
            with open('Error_enviar_embeddings_s3.txt', 'w') as file:
                file.write(str(e))
            raise
        
        return