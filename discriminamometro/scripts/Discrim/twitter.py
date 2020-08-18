import os
import tweepy
import configparser

class Twitter():
    
    def __init__(self):

        self.generar_conexion_twitter()

        return
    
    def generar_conexion_twitter(self):
        
        str_DirectorioActual = os.getcwd()

        config = configparser.ConfigParser()
        config.read(str_DirectorioActual + '/config.txt')
        str_Usuario = config['consumer_tokens']['consumer_key']
        str_Password = config['consumer_tokens']['consumer_secret']
        
        self.auth = tweepy.AppAuthHandler(str_Usuario, str_Password)
        self.api = tweepy.API(self.auth)
        
        return
    
    def obtener_tweets(self, str_Query, nbr_TweetsDescarga):

        list_Tweets = []

        # Se hace el query y se barren los resultados
        for tweet in tweepy.Cursor(self.api.search, q=str_Query, tweet_mode='extended', lang="es", geocode="23.005273,-103.527174,1792km").items(nbr_TweetsDescarga):

            # Agregamos el json a la lista de tweets por categoria
            list_Tweets.append(tweet)

        return list_Tweets
    

