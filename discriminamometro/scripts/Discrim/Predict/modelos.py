import Discrim.Predict.Capa1.discriminacion as discr

import Discrim.Predict.Capa2.apariencia as apar
import Discrim.Predict.Capa2.discapacidad as discap
import Discrim.Predict.Capa2.edad as edad
import Discrim.Predict.Capa2.genero as genero
import Discrim.Predict.Capa2.ideologia as ideo
import Discrim.Predict.Capa2.orientacion as orien
import Discrim.Predict.Capa2.religion as relig

class Modelos():
    
    def __init__(self):
        
        # Capa1
        self.discr = discr.Discriminacion()
        
        # Capa2
        self.apar = apar.Apariencia()
        self.discap = discap.Discapacidad()
        self.edad = edad.Edad()
        self.genero = genero.Genero()
        self.ideo = ideo.Ideologia()
        self.orien = orien.Orientacion()
        self.relig = relig.Religion()
        
        return