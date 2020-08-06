import json
import os
import configparser
import re
import pickle as pickle

from datetime import datetime, timedelta
import time

from pathlib import Path

import pandas as pd
import tweepy
from unidecode import unidecode
import boto3
import nltk
from nltk.corpus import stopwords

class Utileria:

    def __init__(self):

        # S3
        self.str_NombreBucket = 'discriminamometro'

        # Twitter
        self.ObtenerCredencialesTwitter()

        self.str_DirectorioActual = os.getcwd()
        self.str_DirectorioHome = os.environ['HOME']

        return

    def CrearConexionS3(self):

        from boto3 import Session
        session = Session(profile_name='sociedat')

        credentials = session.get_credentials()
        current_credentials = credentials.get_frozen_credentials()

        s3 = boto3.client(
                's3',
                aws_access_key_id=current_credentials.access_key,
                aws_secret_access_key=current_credentials.secret_key,
                aws_session_token=current_credentials.token,
                region_name='us-west-2',  # Oregon
                use_ssl=False
            )

        return s3

    def MandarArchivoS3(self, cnx_S3, bucket_name, str_RutaS3, str_Archivo):

        str_ArchivoEnvio = str_Archivo
        str_NombreArchivoEnS3 = str_RutaS3+os.path.basename(str_Archivo)

        # Mandamos el archivo a S3
        print('str_ArchivoEnvio: ', str_ArchivoEnvio)
        print('str_NombreArchivoEnS3: ', str_NombreArchivoEnS3)

        print('Enviando el archivo a S3...')
        cnx_S3.upload_file(str_ArchivoEnvio, bucket_name, str_NombreArchivoEnS3)

        return

    def ObtenerCredencialesTwitter(self):

        str_DirectorioActual = os.getcwd()
        str_DirectorioHome = os.environ['HOME']

        config = configparser.ConfigParser()
        config.read(str_DirectorioActual + '/config.txt')
        self.str_Usuario = config['consumer_tokens']['consumer_key']
        self.str_Password = config['consumer_tokens']['consumer_secret']

        return

    def GenerarArchivoJSON(self, par_Nombre, par_Contenido):

        # Generamos el archivo json que contiene los tweets con el tema que se está trabajando
        with open(par_Nombre, 'w') as file:

            # Escribimos un archivo por cada categoría (inluimos la hora para)
            file.write(json.dumps(par_Contenido))

        return

    def AbrirJSONComoDataframe(self,str_Path):
        """
        Script para leer los datos y convertirlos en data frame
        Returns:
            data frame
        """

        df = pd.read_json(str_Path)
        df = pd.DataFrame(df)

        return df


class Discriminamometro:

    def __init__(self, par_TipoEjecucion = 'REAL'):

        # print('Utileria Discriminamometro')
        self.Utileria = Utileria()
        self.str_TipoEjecucion = par_TipoEjecucion

        self.auth = tweepy.AppAuthHandler(self.Utileria.str_Usuario, self.Utileria.str_Password)
        self.api = tweepy.API(self.auth)

        # Lista de categorías por parte de la COPRED
        with open("catalogo.json") as f:
            self.dict_Catalogo = json.load(f)

        # Configuramos el número de tweets que se desean descargar por cada corrida
        self.nbr_TweetsXCorrida = 3000

        if par_TipoEjecucion == 'PRUEBA':
            self.nbr_TweetsXCorrida = 8

        self.nbr_CantidadTemas = len(self.dict_Catalogo.keys()) + 1
        self.nbr_TweetsXCategoria = int(self.nbr_TweetsXCorrida/self.nbr_CantidadTemas)

        # Información para cargar el modelo
        self.str_PathCountVecrorizer=''
        self.str_StopWords=''
        self.str_LDA=''

        return

    # Método para generar el registro Json por cada tweet
    def CrearRegistroJson(self, tweet):

        json = {}

        # Se usa un try para obtener el valor si es que proviene de un retweet
        try:
            json =  {
            'user_id': unidecode(tweet.user.id_str),
            'name': unidecode(tweet.user.name),
            'screen_name': unidecode(tweet.user.screen_name),
            'full_text': unidecode(tweet.retweeted_status.full_text),
            'location': unidecode(tweet.user.location)
        }
        except:
        # Si falla el try, significa que no es un retweet (es un tweet normal)
            json =  {
            'user_id': unidecode(tweet.user.id_str),
            'name': unidecode(tweet.user.name),
            'screen_name': unidecode(tweet.user.screen_name),
            'full_text': unidecode(tweet.full_text),
            'location': unidecode(tweet.user.location)
        }

        return json


    def ObtenerTweets(self, str_Query, nbr_TweetsDescarga):

        list_Tweets = []

        # Se hace el query y se barren los resultados
        for tweet in tweepy.Cursor(self.api.search, q=str_Query, tweet_mode='extended', lang="es", geocode="23.005273,-103.527174,1792km").items(nbr_TweetsDescarga):

            # Formateamos el tweet a formato json
            json_Tweet = self.CrearRegistroJson(tweet)

            # Agregamos el json a la lista de tweets por categoria
            list_Tweets.append(json_Tweet)

            # Agregamos el tweet raw a la lista de tweets totales
            # self.list_TweetsTotal.append(tweet)

        return list_Tweets


    def DescargarTweets(self):

        print('Entra a DescargarTweets')
        # self.list_TweetsTotal = []
        self.list_TerminosTodos = []

        # Se barren las categorias
        for str_Categoria, list_Terminos in self.dict_Catalogo.items():

            #print()
            #print(str_Categoria)

            # Mostramos los términos correspondientes al tema
            #print(list_Terminos)

            str_Query = self.FormatearQuery(list_Terminos)
            #print(str_Query)

            list_TweetsCategoria = []
            list_TweetsCategoria = self.ObtenerTweets(str_Query, self.nbr_TweetsXCategoria)

            str_IdArchivo = self.ArmarNombreArchivo(str_Categoria)

            # Se genera el archivo JSON
            self.Utileria.GenerarArchivoJSON(str_IdArchivo, list_TweetsCategoria)

            # Se envía el archivo a S3
            self.EnviarArchivoS3(str_IdArchivo, str_Categoria)

            # Una vez enviado el archivo, lo eliminamos localmente
            os.system('rm ' + str_IdArchivo)

            # Se prepara la categoría neutra
            for termino in list_Terminos:
                self.list_TerminosTodos.append(termino)

        # Se genera el archivo neutro
        list_TweetsSinFiltro = self.ObtenerTweets(' ', self.nbr_TweetsXCategoria)
        list_TweetsNeutros = self.RemoverTweetsDiscriminantes(list_TweetsSinFiltro)

        str_Categoria = 'neutro'
        str_IdArchivo = self.ArmarNombreArchivo(str_Categoria)
        self.Utileria.GenerarArchivoJSON(str_IdArchivo, list_TweetsNeutros)

        self.EnviarArchivoS3(str_IdArchivo, str_Categoria)
        os.system('rm ' + str_IdArchivo)

        return

    def FormatearQuery(self, par_Terminos):

        str_QueryFormat = ''

        for termino in par_Terminos:
            str_QueryFormat = str_QueryFormat + '"' + termino + '"' + ' OR '

        str_QueryFormat = str_QueryFormat[ 0:len(str_QueryFormat) - 4 ]

        return str_QueryFormat

    def ArmarNombreArchivo(self, par_Tema):

        date_time = datetime.fromtimestamp(time.time())
        str_IdentificadorDttm = str(date_time).replace('-','').replace(' ','_').replace('.','').replace(':','')
        str_IdArchivo = 'json_' + par_Tema + '_' + str_IdentificadorDttm + '.txt'
        str_IdArchivo = self.Utileria.str_DirectorioActual + '/' + str_IdArchivo

        return str_IdArchivo

    def EnviarArchivoS3(self, par_Archivo, par_Categoria):

        # Una vez generado el archivo, lo envíamos a S3
        cnx_S3 = self.Utileria.CrearConexionS3()
        str_ArchivoLocal = par_Archivo
        str_RutaS3 = par_Categoria + '/'

        # Temporalmente mandamos todo a la carpeta 00_pruebas
        # str_RutaS3 = '00_pruebas/'

        # Mandamos el archivo descargado a S3
        try:
            self.Utileria.MandarArchivoS3(cnx_S3, self.Utileria.str_NombreBucket, str_RutaS3, str_ArchivoLocal)
        except Exception as e:
            with open('ErrorEnviosS3.txt', 'w') as file:
                file.write(str(e))
            raise

        return

    def RemoverTweetsDiscriminantes(self, par_Tweets):

        list_TweetsNeutros = []
        for tweet in par_Tweets:

            # Evaluamos si cada tweet tiene terminos discriminantes
            if not self.TieneTerminosDiscriminantes(tweet['full_text']):
                list_TweetsNeutros.append(tweet)

        return list_TweetsNeutros

    def TieneTerminosDiscriminantes(self, par_Texto):

        bool_TerminoEncontrado = False

        # Se recorre la lista que tienen todos los terminos juntos
        for termino in self.list_TerminosTodos:
            if par_Texto.find(termino) > -1:
                bool_TerminoEncontrado = True
                break

        return bool_TerminoEncontrado


    def QuitarStopWordsDataFrame(self, par_DataFrame, par_Idioma = 'spanish', par_Columna = 'full_text'):
        """
        Quita stop wors, se pueden añadir más palabras al pickle
        Returns:
            documento limpio
        """

        # Se obtienen las stopwords desde un archivo pickle
        self.CargarStopWords()
        # ickleFile = open('StopWords.p', 'rb')
        # stop_words = pickle.load(pickleFile)
        # pickleFile.close()

        # Se deberá agregar una validación para que en caso de que no se encuentre el pickle, descargar las stop words
        # nltk.download('stopwords')
        # self.stop_words = set(stopwords.words(par_Idioma))

        pd.options.mode.chained_assignment = None
        listaAux = par_DataFrame['full_text'].values.tolist()

        for i in range(len(par_DataFrame[par_Columna])):
            # if i%1000 == 0:
            #     print(i)

            listaAux[i] = " ".join([word for word in str(listaAux[i]).split()
                      if word not in self.stop_words])

        par_DataFrame[par_Columna] = listaAux
        return par_DataFrame

    def LimpiarDataFrame(self, par_Dataframe, par_Columna = 'full_text'):
        # TODO: Pensar si debemos quitar o no los hashtags
        """
        Limpia los tweet de forma genérica.
            1. pasa el texto a minúsculas
            2. quita url
            3. quita "@" y "RT" del texto
        Returns:
            documento limpio
        """

        pd.options.mode.chained_assignment = None
        listaAux = par_Dataframe['full_text'].values.tolist()

        for i in range(len(par_Dataframe[par_Columna])):
            # if i%10000 == 0:
            #     print(i)
            listaAux[i] = " ".join([word for word in str(listaAux[i]).split()
                      if 'http' not in word and '@' not in word and '<' not in word and 'RT' not in word and 'rt' not in word and '"' not in word])

        par_Dataframe[par_Columna] = listaAux
        par_Dataframe[par_Columna] = par_Dataframe[par_Columna].apply(lambda x: re.sub('[¡!@#$:).;,¿?&\']', '', x.lower()))
        par_Dataframe[par_Columna] = par_Dataframe[par_Columna].apply(lambda x: re.sub('  ', ' ', x))

        return par_Dataframe

    def CargarStopWords(self):

        pickleFile = open(self.str_StopWords, 'rb')
        self.stop_words = pickle.load(pickleFile)
        pickleFile.close()

    def CargarPicklesModeloLDA(self):

        pickleFile = open(self.str_LDA, 'rb')
        self.lda = pickle.load(pickleFile)
        pickleFile.close()

        pickleFile = open(self.str_PathCountVecrorizer, 'rb')
        self.count_vectorizer = pickle.load(pickleFile)
        pickleFile.close()

        return

    def DeterminarCategorias_X_Texto(self, par_Texto):

        arr_Ponderaciones = self.lda.transform(self.count_vectorizer.transform([par_Texto]))

        return arr_Ponderaciones

    def DeterminarCategorias_X_HashTag(self, par_Query):

        list_Tweets = []
        list_Tweets = self.ObtenerTweets(par_Query, 3)

        # Generamos una propiedad en la clase para poder revisar los tweets devueltos por la consulta
        self.list_Tweets_X_HT = list_Tweets

        # Se convierte en dataframe la lista de tweets obtenidos
        df = pd.DataFrame(list_Tweets)
        df = self.LimpiarDataFrame(df)
        df = self.QuitarStopWordsDataFrame(df)

        df2 = df['full_text'].apply(self.DeterminarCategorias_X_Texto)

        # Se guarda en un atributo el promedio de ponderaciones
        self.arr_Ponderaciones_X_HT = df2.mean()

        return

    def DeterminarCategorias_X_Usuario(self, par_Usuario):

        list_Tweets = []

        for tweet in tweepy.Cursor(self.api.user_timeline, screen_name=par_Usuario, tweet_mode="extended").items(3):

            # Formateamos el tweet a formato json
            json_Tweet = self.CrearRegistroJson(tweet)

            list_Tweets.append(json_Tweet)

        # Generamos una propiedad en la clase para poder revisar los tweets devueltos por la consulta
        self.list_Tweets_X_Usuario = list_Tweets

        # Se convierte en dataframe la lista de tweets obtenidos
        df = pd.DataFrame(list_Tweets)
        df = self.LimpiarDataFrame(df)
        df = self.QuitarStopWordsDataFrame(df)

        df2 = df['full_text'].apply(self.DeterminarCategorias_X_Texto)

        # Se guarda en un atributo el promedio de ponderaciones
        self.arr_Ponderaciones_X_Usuario = df2.mean()

        return
