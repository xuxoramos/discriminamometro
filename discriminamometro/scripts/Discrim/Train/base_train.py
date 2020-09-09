import Discrim.utileria as ut
import pickle as pickle
import Discrim.Train.magic_loop as mgl
import pandas as pd
from sklearn.model_selection import train_test_split

class BaseTrain():
    
    def __init__(self):
        
        # Cargamos la utilería para realizar todos los procesos
        self.obj_utileria = ut.Utileria()
        self.obj_utileria.cargar_modelo_embeddings()
        self.obj_utileria.cargar_stop_words()
        self.obj_utileria.descargar_punkt()
        
        return
    
    def descargar_tweets_entrenamiento(self):
        
        s3 = self.obj_utileria.crear_conexion_s3()
        
        with open(self.str_LocalFile, 'wb') as f:
            s3.download_fileobj(self.obj_utileria.str_NombreBucket,  self.str_ruta_entrenamiento+'/'+self.str_fuente_clasificacion, f)
        
        return
    
    def transformar_dataset(self):
        
        # self.pd_fuente = pd.read_csv('tmp_fuente_embeddings.csv', lineterminator='\n') 
        self.pd_fuente = pd.read_csv(self.str_LocalFile, lineterminator='\n') 
                
        self.pd_fuente = self.obj_utileria.formatear_dataframe(self.pd_fuente)
        
        return
    
    def train(self):
        
        self.train, self.test = train_test_split(self.pd_fuente, test_size=0.2,random_state = 202008)
        
        obj_mgl = mgl.MagicLoop()
        
        X_train = pd.DataFrame(self.train.embeddings.tolist())
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
        
        fuente['embeddings'] = list(npEmbeddings)
        return fuente 
    
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
    
   