import json
from Discriminamometro import Utileria, Discriminamometro

def lambda_handler(event, context):
    # TODO implement
    
    # Se instancia el objeto
    obj_Discr = Discriminamometro()
    
    # Se cacha el tipo de petición
    str_Tipo = event['peticion']
    arr = (0)
    bool_Peticion_Valida = False
    
    # De acuerdo al tipo de petición, se manda a llamar al método correspondiente de la clase
    if str_Tipo == 'hrs':
        str_Valor = event['hrs']
        bool_Peticion_Valida = True
    
    elif str_Tipo == 'ht':
        str_Valor = event['ht']
        arr = obj_Discr.DeterminarCategorias_X_HashTag(str_Valor)
        bool_Peticion_Valida = True
    
    elif str_Tipo == 'usuario':
        str_Valor = event['usuario']
        arr = obj_Discr.DeterminarCategorias_X_Usuario(str_Valor)
        bool_Peticion_Valida = True
        
    elif str_Tipo == 'texto':
        str_Valor = event['texto']
        arr = obj_Discr.DeterminarCategorias_X_Texto(str_Valor)
        bool_Peticion_Valida = True
        
    if bool_Peticion_Valida == True:
        return {
        'statusCode': 200,
        'body': json.dumps(arr)
        }
    else:
        return {
        'statusCode': 200,
        'body': "Petición inválida"
        }
