import Discrim.Train.Capa2.apariencia as apa
import Discrim.Train.Capa2.discapacidad as disc
import Discrim.Train.Capa2.edad as ed
import Discrim.Train.Capa2.genero as gen
import Discrim.Train.Capa2.ideologia as ideo
import Discrim.Train.Capa2.orientacion as orien
import Discrim.Train.Capa2.religion as relig

def apariencia():
    
    obj_apariencia = apa.Apariencia()
    obj_apariencia.descargar_tweets_entrenamiento()
    obj_apariencia.transformar_dataset()
    obj_apariencia.train()
    obj_apariencia.crear_pickle()
    obj_apariencia.mandar_pickle_s3()
    
    return

def discapacidad():

    obj_discapacidad = disc.Discapacidad()
    obj_discapacidad.descargar_tweets_entrenamiento()
    obj_discapacidad.transformar_dataset()
    obj_discapacidad.train()
    obj_discapacidad.crear_pickle()
    obj_discapacidad.mandar_pickle_s3()
    
    return

def edad():

    obj_edad = ed.Edad()
    obj_edad.descargar_tweets_entrenamiento()
    obj_edad.transformar_dataset()
    obj_edad.train()
    obj_edad.crear_pickle()
    obj_edad.mandar_pickle_s3()

    return

def genero():
    
    obj_genero = gen.Genero()
    obj_genero.descargar_tweets_entrenamiento()
    obj_genero.transformar_dataset()
    obj_genero.train()
    obj_genero.crear_pickle()
    obj_genero.mandar_pickle_s3()
    
    return

def ideologia():

    obj_ideologia = ideo.Ideologia()
    obj_ideologia.descargar_tweets_entrenamiento()
    obj_ideologia.transformar_dataset()
    obj_ideologia.train()
    obj_ideologia.crear_pickle()
    obj_ideologia.mandar_pickle_s3()
    
    return

def orientacion():

    obj_orientacion = orien.Orientacion()
    obj_orientacion.descargar_tweets_entrenamiento()
    obj_orientacion.transformar_dataset()
    obj_orientacion.train()
    obj_orientacion.crear_pickle()
    obj_orientacion.mandar_pickle_s3()
    
    return

def religion():

    obj_religion = relig.Religion()
    obj_religion.descargar_tweets_entrenamiento()
    obj_religion.transformar_dataset()
    obj_religion.train()
    obj_religion.crear_pickle()
    obj_religion.mandar_pickle_s3()
    
    return

if __name__== "__main__" :

    try:
    
        # La llamada a cada entrenamiento está acomodada del más rápido al más tardado
        religion()
        edad()
        discapacidad()
        ideologia()
        apariencia()
        orientacion()
        genero()
    
    # Si llega a tronar algo, cachamos el error y lo escribimos en el archivo log para saber qué fue
    except Exception as err:
        with open('script_entrenamiento_error.txt', 'w') as file:
            file.write(str(err))


