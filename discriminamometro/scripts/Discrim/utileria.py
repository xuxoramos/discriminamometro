import pandas as pd
import boto3
import os
import pickle as pickle
import dask.dataframe as dd
import re


class Utileria:

    def __init__(self):

        # S3
        self.str_NombreBucket = 'discriminamometro'
        self.str_StopWords = 'StopWords.p'
        self.str_DirectorioActual = os.getcwd()
        self.nbr_cpu = os.cpu_count() 

        return

    def crear_conexion_s3(self):

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

    def mandar_archivo_s3(self, cnx_S3, bucket_name, str_RutaS3, str_Archivo):

        str_ArchivoEnvio = str_Archivo
        str_NombreArchivoEnS3 = str_RutaS3+os.path.basename(str_Archivo)

        # Mandamos el archivo a S3
        print('str_ArchivoEnvio: ', str_ArchivoEnvio)
        print('str_NombreArchivoEnS3: ', str_NombreArchivoEnS3)

        print('Enviando el archivo a S3...')
        cnx_S3.upload_file(str_ArchivoEnvio, bucket_name, str_NombreArchivoEnS3)
        print('Envío completado')

        return

    def abrir_json_como_dataframe(self,str_Path):
        """
        Script para leer los datos y convertirlos en data frame
        Returns:
            data frame
        """

        df = pd.read_json(str_Path)
        df = pd.DataFrame(df)

        return df
    
    def quitar_stop_words_dataframe(self, par_DataFrame, par_Idioma = 'spanish', par_Columna = 'full_text'):
        """
        Quita stop wors, se pueden añadir más palabras al pickle
        Returns:
            documento limpio
        """

        pd.options.mode.chained_assignment = None
        listaAux = par_DataFrame['full_text'].values.tolist()

        for i in range(len(par_DataFrame[par_Columna])):
            # if i%1000 == 0:
            #     print(i)

            listaAux[i] = " ".join([word for word in str(listaAux[i]).split()
                      if word not in self.stop_words])

        par_DataFrame[par_Columna] = listaAux
        return par_DataFrame
    
    def limpiar_dataframe(self, par_Dataframe, par_Columna = 'full_text'):
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
        
    def cargar_stop_words(self):
        
        s3 = self.crear_conexion_s3()
        
        str_LocalFile = 'tmp_Stopwords.p'
        with open(str_LocalFile, 'wb') as f:
            s3.download_fileobj(self.str_NombreBucket, self.str_StopWords, f)

        pickleFile = open(str_LocalFile, 'rb')
        self.stop_words = pickle.load(pickleFile)
        pickleFile.close()
        
        os.remove(str_LocalFile)
        
    def formatear_dataframe(self, dataset):
        
        ddf = dd.from_pandas(dataset, npartitions=self.nbr_cpu)        
        dataset = ddf.map_partitions(self.limpiar_dataframe, meta=ddf).compute()
        
        ddf = dd.from_pandas(dataset, npartitions=self.nbr_cpu)
        dataset = ddf.map_partitions(self.quitar_stop_words_dataframe, meta=ddf).compute()
        
        return dataset