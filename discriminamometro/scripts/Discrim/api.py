import Discrim.Predict.modelos as mod
import Discrim.utileria as ut
import pandas as pd
import Discrim.twitter as tw

class API():
    
    def __init__(self):
        
        # Cargamos la clase que hace las peticiones a twitter
        self.obj_twitter = tw.Twitter()
        
        # Cargamos todos los modelos
        self.obj_modelos = mod.Modelos()
        
        # Cargamos la utilería para realizar todos los procesos
        self.obj_utileria = ut.Utileria()
        self.obj_utileria.cargar_modelo_embeddings()
        self.obj_utileria.cargar_stop_words()
        self.obj_utileria.descargar_punkt()
        
        self.nbr_tweets_x_hrs = 1
        self.nbr_tweets_x_ht = 3
        self.nbr_tweets_x_usr = 1
        
        return
    
    def clasificar_x_horas(self, nbr_horas):
        
        return
    
    def clasificar_x_ht(self, str_ht):
        
        str_Query = str_ht
        
        list_Tweets = []
        list_Tweets = self.obj_twitter.obtener_tweets(str_Query, self.nbr_tweets_x_ht)
        
        list_Formateada = []
        for tweet in list_Tweets:
            tweet_json = self.obj_utileria.crear_registro_json(tweet)
            list_Formateada.append(tweet_json)

        # Almacenamos el dataframe en la clase para poder consultarlo desde afuera (para pruebas)
        self.list_Formateada = list_Formateada
        
        # Se crea el dataframe
        df = pd.DataFrame(list_Formateada)
        
        # Se prepara para la predicción
        df = self.obj_utileria.formatear_dataframe(df)
        
        # Almacenamos el dataframe en la clase para poder consultarlo desde afuera (para pruebas)
        self.df = df
        
        # Convertimos la columna a lista
        X_predict = df.embeddings.tolist()
        
        # Almacenamos el dataframe en la clase para poder consultarlo desde afuera (para pruebas)
        self.X_predict = X_predict
        
        # Llamamos al método que va a clasificar el arreglo con todos los modelos
        rslt = self.clasificar_arr(X_predict)
        
        return rslt
    
    def clasificar_x_usuario(self, str_usuario):

        # Se prepara para la predicción
        df = self.obj_utileria.formatear_dataframe(df)
        
        # Convertimos la columna a lista
        X_predict = df.embeddings.tolist()
        
        # Llamamos al método que va a clasificar el arreglo con todos los modelos
        rslt = self.clasificar_arr(X_predict)
        
        # Almacenamos el dataframe en la clase para poder consultarlo desde afuera (para pruebas)
        self.df = df
        self.X_predict = X_predict
        
        return rslt
    
    def clasificar_x_texto(self, str_Texto):
        
        # Initialise data to lists. 
        data = [{'full_text': str_Texto}] 

        self.proceso_prediccion(data)
        
        return self.rslt
    
    def proceso_prediccion(self, list_data):
                
        # Se crea el dataframe tomando una lista como parámetro
        df = pd.DataFrame(list_data)

        # Se prepara para la predicción
        self.df = self.obj_utileria.formatear_dataframe(df)
        
        # Convertimos la columna embeddings a lista
        self.X_predict = self.df.embeddings.tolist()
                
        # Llamamos al método que va a clasificar el arreglo con todos los modelos
        self.rslt = self.clasificar_arr(self.X_predict)
        
        return
    
    def clasificar_arr(self, X_predict):
        
        dict_scores = {'discriminacion':0
              ,'apariencia':1
              ,'discapacidad':2
              ,'edad':3
              ,'genero':4
              ,'ideologia':5
              ,'orientacion':6
              ,'religion':7}
        
        # Barremos el diccionario para utilizar todos los modelos sobre cada registro
        for k,it in dict_scores.items():
            
            if k == 'discriminacion':
                dict_scores.update({k: self.obj_modelos.discr.modelo.predict_proba(X_predict)})
            elif k == 'apariencia':
                dict_scores.update({k: self.obj_modelos.apar.modelo.predict_proba(X_predict)})                               
            elif k == 'discapacidad':
                dict_scores.update({k: self.obj_modelos.discap.modelo.predict_proba(X_predict)})                
            elif k == 'edad':
                dict_scores.update({k: self.obj_modelos.edad.modelo.predict_proba(X_predict)})                
            elif k == 'genero':
                dict_scores.update({k: self.obj_modelos.genero.modelo.predict_proba(X_predict)})                
            elif k == 'ideologia':
                dict_scores.update({k: self.obj_modelos.ideo.modelo.predict_proba(X_predict)})                
            elif k == 'orientacion':
                dict_scores.update({k: self.obj_modelos.orien.modelo.predict_proba(X_predict)})                
            elif k == 'religion':
                dict_scores.update({k: self.obj_modelos.relig.modelo.predict_proba(X_predict)})                
                
        return dict_scores