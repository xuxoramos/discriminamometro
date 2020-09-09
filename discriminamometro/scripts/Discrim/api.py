import Discrim.Predict.modelos as mod
import Discrim.utileria as ut
import pandas as pd
import Discrim.twitter as tw
from datetime import *

class API():
    
    def __init__(self, nbr_tweets_x_hrs = 2, nbr_tweets_x_ht = 3, nbr_tweets_x_usr = 4):
        
        # Cargamos la clase que hace las peticiones a twitter
        self.obj_twitter = tw.Twitter()
        
        # Cargamos todos los modelos
        self.obj_modelos = mod.Modelos()
        
        # Cargamos la utilería para realizar todos los procesos
        self.obj_utileria = ut.Utileria()
        self.obj_utileria.cargar_modelo_embeddings()
        self.obj_utileria.cargar_stop_words()
        self.obj_utileria.descargar_punkt()
        
        self.nbr_tweets_x_hrs = nbr_tweets_x_hrs
        self.nbr_tweets_x_ht = nbr_tweets_x_ht
        self.nbr_tweets_x_usr = nbr_tweets_x_usr
        
        return
    
    def clasificar_x_horas(self, nbr_horas):
        
        dttm_desde = datetime.now() + timedelta(hours = nbr_horas)
        
        list_Tweets = []
        list_Tweets = self.obj_twitter.obtener_tweets('', self.nbr_tweets_x_hrs)
        
        list_Formateada = []
        for tweet in list_Tweets:
            
            # Sólo se toman los tweets que están en el rango de tiempo solicitado
            if dttm_desde <= tweet.created_at:
                tweet_json = self.obj_utileria.crear_registro_json(tweet)
                list_Formateada.append(tweet_json)
        
        self.proceso_prediccion(list_Formateada)
        
        return self.rslt
        
        return
    
    def clasificar_x_ht(self, str_ht):
        
        str_Query = str_ht
        
        list_Tweets = []
        list_Tweets = self.obj_twitter.obtener_tweets(str_Query, self.nbr_tweets_x_ht)
        
        list_Formateada = []
        for tweet in list_Tweets:
            tweet_json = self.obj_utileria.crear_registro_json(tweet)
            list_Formateada.append(tweet_json)
        
        self.proceso_prediccion(list_Formateada)
        
        return self.rslt
    
    def clasificar_x_usuario(self, str_usuario):
        
        str_Query = str_usuario
        
        list_Tweets = []
        list_Tweets = self.obj_twitter.obtener_tweets_usuario(str_Query, self.nbr_tweets_x_usr)
        
        list_Formateada = []
        for tweet in list_Tweets:
            tweet_json = self.obj_utileria.crear_registro_json(tweet)
            list_Formateada.append(tweet_json)

        self.proceso_prediccion(list_Formateada)
        
        return self.rslt
    
    def clasificar_x_texto(self, str_Texto):
        
        # Initialise data to lists. 
        data = [{'full_text': str_Texto}] 

        self.proceso_prediccion(data)
        
        return self.rslt
    
    def proceso_prediccion(self, list_data):
        
        self.list_data = list_data
        
        # Se crea el dataframe tomando una lista como parámetro
        self.df = pd.DataFrame(self.list_data)

        # Se prepara para la predicción
        self.df = self.obj_utileria.formatear_dataframe(self.df)
        
        # Convertimos la columna embeddings a lista
        self.X_predict = self.df.embeddings.tolist()
                
        # Llamamos al método que va a clasificar el arreglo con todos los modelos
        self.rslt = self.clasificar_arr(self.X_predict)
        
        return
    
    def clasificar_arr(self, X_predict):
        
        dict_scores = {'discriminacion':0
              ,'apariencia':0
              ,'discapacidad':0
              ,'edad':0
              ,'genero':0
              ,'ideologia':0
              ,'orientacion':0
              ,'religion':0}
        
        # Barremos el diccionario para utilizar todos los modelos sobre cada registro
        for k,it in dict_scores.items():
            
            if k == 'discriminacion':
                dict_scores.update({k: self.obj_modelos.discr.modelo.predict_proba(X_predict).tolist()})
            elif k == 'apariencia':
                dict_scores.update({k: self.obj_modelos.apar.modelo.predict_proba(X_predict).tolist()})                           
            elif k == 'discapacidad':
                dict_scores.update({k: self.obj_modelos.discap.modelo.predict_proba(X_predict).tolist()})                
            elif k == 'edad':
                dict_scores.update({k: self.obj_modelos.edad.modelo.predict_proba(X_predict).tolist()})                
            elif k == 'genero':
                dict_scores.update({k: self.obj_modelos.genero.modelo.predict_proba(X_predict).tolist()})                
            elif k == 'ideologia':
                dict_scores.update({k: self.obj_modelos.ideo.modelo.predict_proba(X_predict).tolist()})                
            elif k == 'orientacion':
                dict_scores.update({k: self.obj_modelos.orien.modelo.predict_proba(X_predict).tolist()})                
            elif k == 'religion':
                dict_scores.update({k: self.obj_modelos.relig.modelo.predict_proba(X_predict).tolist()})                
                
        return dict_scores