import Discrim.twitter as tw
import Discrim.utileria as ut
import json
from datetime import datetime, timedelta
import time
from unidecode import unidecode
import os

class Etl():
    
    def __init__(self, par_TipoEjecucion = 'PRUEBA'):
        
        self.obj_utileria = ut.Utileria()

        # Configuramos el número de tweets que se desean descargar por cada corrida
        if par_TipoEjecucion == 'PRUEBA':
            self.nbr_TweetsXCorrida = 8
        elif par_TipoEjecucion == 'REAL':
            self.nbr_TweetsXCorrida = 3000
            
        return
    
    def descarga_recurrente_tweets(self):

        print('Entra a descarga_recurrente_tweets')
        
        obj_twitter = tw.Twitter()
        
        # Lista de categorías por parte de la COPRED
        with open("catalogo.json") as f:
            self.dict_Catalogo = json.load(f)
        
        self.nbr_CantidadTemas = len(self.dict_Catalogo.keys()) + 1
        self.nbr_TweetsXCategoria = int(self.nbr_TweetsXCorrida/self.nbr_CantidadTemas)
        
        # self.list_TweetsTotal = []
        self.list_TerminosTodos = []

        # Se barren las categorias
        for str_Categoria, list_Terminos in self.dict_Catalogo.items():

            #print()
            #print(str_Categoria)

            # Mostramos los términos correspondientes al tema
            #print(list_Terminos)

            str_Query = self.formatear_query(list_Terminos)
            #print(str_Query)

            list_TweetsCategoria = []
            list_TweetsCategoria = obj_twitter.obtener_tweets(str_Query, self.nbr_TweetsXCategoria)
            
            list_Formateada = []
            for tweet in list_TweetsCategoria:
                tweet_json = self.obj_utileria.crear_registro_json(tweet)
                list_Formateada.append(tweet_json)
                
            list_TweetsCategoria = list_Formateada

            str_IdArchivo = self.armar_nombre_archivo(str_Categoria)

            # Se genera el archivo JSON
            self.generar_archivo_json(str_IdArchivo, list_TweetsCategoria)

            # Se envía el archivo a S3
            self.enviar_archivo_s3(str_IdArchivo, str_Categoria)

            # Una vez enviado el archivo, lo eliminamos localmente
            os.system('rm ' + str_IdArchivo)

            # Se prepara la categoría neutra
            for termino in list_Terminos:
                self.list_TerminosTodos.append(termino)

        # Se genera el archivo neutro
        list_TweetsSinFiltro = obj_twitter.obtener_tweets(' ', self.nbr_TweetsXCategoria)
        
        list_Formateada = []
        for tweet in list_TweetsSinFiltro:
            tweet_json = self.obj_utileria.crear_registro_json(tweet)
            list_Formateada.append(tweet_json)
        list_TweetsSinFiltro = list_Formateada
                
        list_TweetsNeutros = self.remover_tweets_discriminantes(list_TweetsSinFiltro)

        str_Categoria = 'neutro'
        str_IdArchivo = self.armar_nombre_archivo(str_Categoria)
        self.generar_archivo_json(str_IdArchivo, list_TweetsNeutros)

        self.enviar_archivo_s3(str_IdArchivo, str_Categoria)
        os.system('rm ' + str_IdArchivo)

        return
    
    def formatear_query(self, par_Terminos):

        str_QueryFormat = ''

        for termino in par_Terminos:
            str_QueryFormat = str_QueryFormat + '"' + termino + '"' + ' OR '

        str_QueryFormat = str_QueryFormat[ 0:len(str_QueryFormat) - 4 ]

        return str_QueryFormat
        
    def armar_nombre_archivo(self, par_Tema):

        date_time = datetime.fromtimestamp(time.time())
        str_IdentificadorDttm = str(date_time).replace('-','').replace(' ','_').replace('.','').replace(':','')
        str_IdArchivo = 'json_' + par_Tema + '_' + str_IdentificadorDttm + '.txt'
        str_IdArchivo = self.obj_utileria.str_DirectorioActual + '/' + str_IdArchivo

        return str_IdArchivo
    
    def generar_archivo_json(self, par_Nombre, par_Contenido):

        # Generamos el archivo json que contiene los tweets con el tema que se está trabajando
        with open(par_Nombre, 'w') as file:

            # Escribimos un archivo por cada categoría (inluimos la hora para)
            file.write(json.dumps(par_Contenido))

        return
    
    def enviar_archivo_s3(self, par_Archivo, par_Categoria):

        # Una vez generado el archivo, lo envíamos a S3
        
        cnx_S3 = self.obj_utileria.crear_conexion_s3()
        str_ArchivoLocal = par_Archivo
        str_RutaS3 = par_Categoria + '/'

        # Temporalmente mandamos todo a la carpeta 00_pruebas
        str_RutaS3 = '00_pruebas/'

        # Mandamos el archivo descargado a S3
        try:
            self.obj_utileria.mandar_archivo_s3(cnx_S3, self.obj_utileria.str_NombreBucket, str_RutaS3, str_ArchivoLocal)
        except Exception as e:
            with open('ErrorEnviosS3.txt', 'w') as file:
                file.write(str(e))
            raise

        return
    
    def remover_tweets_discriminantes(self, par_Tweets):

        list_TweetsNeutros = []
        for tweet in par_Tweets:

            # Evaluamos si cada tweet tiene terminos discriminantes
            if not self.tiene_terminos_discriminantes(tweet['full_text']):
                list_TweetsNeutros.append(tweet)

        return list_TweetsNeutros

    def tiene_terminos_discriminantes(self, par_Texto):

        bool_TerminoEncontrado = False

        # Se recorre la lista que tienen todos los terminos juntos
        for termino in self.list_TerminosTodos:
            if par_Texto.find(termino) > -1:
                bool_TerminoEncontrado = True
                break

        return bool_TerminoEncontrado

