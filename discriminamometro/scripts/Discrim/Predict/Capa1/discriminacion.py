from Discrim.Predict import base_modelos

class Discriminacion(base_modelos.BasePredict):
    
    def __init__(self):
        
        # Instanciamos la clase padre
        super().__init__()
        
        # Escribimos la información referente a esta clase
        self.str_ruta_modelo_s3 = '01_modelos/capa1/modelo_capa1.p'
        self.str_archivo_modelo_local = 'modelo_capa1.p'
        
        # Descargamos de s3 y cargamos el modelo correspondiente
        self.descargar_modelo()
        self.cargar_modelo()
        
        return