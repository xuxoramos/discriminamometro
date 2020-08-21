import Discrim.Train.Capa2.apariencia as apa
import Discrim.Train.Capa2.discapacidad as disc
import Discrim.Train.Capa2.edad as ed
import Discrim.Train.Capa2.genero as gen
import Discrim.Train.Capa2.ideologia as ideo
import Discrim.Train.Capa2.orientacion as orien
import Discrim.Train.Capa2.religion as relig

def apariencia():
    
    print("inicio apariencia")
    obj_apariencia = apa.Apariencia()
    print("inicia descarga apariencia")
    obj_apariencia.descargar_tweets_entrenamiento()
    print("inicia tranformar apariencia")
    obj_apariencia.transformar_dataset()
    print("inicia train apariencia")
    obj_apariencia.train()
    print("inicia crear_pickle apariencia")
    obj_apariencia.crear_pickle()
    print("inicia mandar a s3 apariencia")
    obj_apariencia.mandar_pickle_s3()
    print("fin apariencia")
    return

def discapacidad(X_train):

    obj_discapacidad = disc.Discapacidad()
    obj_discapacidad.descargar_tweets_entrenamiento()
    obj_discapacidad.transformar_dataset()
    obj_discapacidad.train(X_train)
    obj_discapacidad.crear_pickle()
    obj_discapacidad.mandar_pickle_s3()
    
    return

def edad(X_train):

    obj_edad = ed.Edad()
    obj_edad.descargar_tweets_entrenamiento()
    obj_edad.transformar_dataset()
    obj_edad.train(X_train)
    obj_edad.crear_pickle()
    obj_edad.mandar_pickle_s3()

    return

def genero(X_train):
    
    obj_genero = gen.Genero()
    obj_genero.descargar_tweets_entrenamiento()
    obj_genero.transformar_dataset()
    obj_genero.train(X_train)
    obj_genero.crear_pickle()
    obj_genero.mandar_pickle_s3()
    
    return

def ideologia(X_train):

    obj_ideologia = ideo.Ideologia()
    obj_ideologia.descargar_tweets_entrenamiento()
    obj_ideologia.transformar_dataset()
    obj_ideologia.train(X_train)
    obj_ideologia.crear_pickle()
    obj_ideologia.mandar_pickle_s3()
    
    return

def orientacion(X_train):

    obj_orientacion = orien.Orientacion()
    obj_orientacion.descargar_tweets_entrenamiento()
    obj_orientacion.transformar_dataset()
    obj_orientacion.train(X_train)
    obj_orientacion.crear_pickle()
    obj_orientacion.mandar_pickle_s3()
    
    return

def religion(X_train):

    obj_religion = relig.Religion()
    obj_religion.descargar_tweets_entrenamiento()
    obj_religion.transformar_dataset()
    obj_religion.train(X_train)
    obj_religion.crear_pickle()
    obj_religion.mandar_pickle_s3()
    
    return

if __name__== "__main__" :

    #try:
    
        # apariencia()

    obj_apariencia = apa.Apariencia()
    obj_apariencia.descargar_tweets_entrenamiento()
    obj_apariencia.transformar_dataset()
    obj_apariencia.train()
    obj_apariencia.crear_pickle()
    obj_apariencia.mandar_pickle_s3()

    #religion('')
    #edad('')
    #discapacidad('obj_apariencia.X_train')
    #ideologia('')
    #apariencia('')
    #orientacion('')
    #genero('obj_apariencia.X_train')
    
    # Si llega a tronar algo, cachamos el error y lo escribimos en el archivo log para saber qué fue
    #except Exception as err:
        #with open('script_entrenamiento_error.txt', 'w') as file:
            #file.write(str(err))


