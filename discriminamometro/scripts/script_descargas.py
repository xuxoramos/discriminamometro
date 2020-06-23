
try:
    
    from Discriminamometro import Utileria, Discriminamometro
    
    # Se instancia la clase del Discriminamometro
    obj_Discr = Discriminamometro('REAL')
    
    # Se manda llamar el proceso de descarga de tweets
    obj_Discr.DescargarTweets()

except Exception as err:
    with open('web_scraping_error.txt', 'w') as file:

        # Escribimos un archivo por cada categoría (inluimos la hora para)
        file.write(str(err))