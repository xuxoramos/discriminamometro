import Discrim.utileria as ut
import pickle as pickle

class BasePredict():
    
    def __init__(self):
        
        self.obj_utileria = ut.Utileria()
        self.str_ruta_modelo_s3 = ''
        self.str_archivo_modelo_local = ''
        
        return
    
    def descargar_modelo(self):
        
        s3 = self.obj_utileria.crear_conexion_s3()
        
        with open(self.str_archivo_modelo_local, 'wb') as f:
            s3.download_fileobj(self.obj_utileria.str_NombreBucket,  self.str_ruta_modelo_s3, f)
        
        return
    
    def cargar_modelo(self):
        
        ################### Carga de parámetros
        pickleFile = open(self.str_archivo_modelo_local, 'rb')
        self.modelo = pickle.load(pickleFile)
        pickleFile.close()
        
        return
    
    def predecir(self):
    
        return