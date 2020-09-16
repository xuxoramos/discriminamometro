try:
    
    import Discrim.etl as etl
    
    # Se instancia la clase encargada del proceso ETL
    obj_etl = etl.Etl('REAL')
    
    # Se manda llamar el proceso de descarga de tweets
    obj_etl.descarga_recurrente_tweets()

except Exception as err:
    with open('web_scraping_error.txt', 'w') as file:

        # Escribimos un archivo por cada categoría (inluimos la hora para)
        file.write(str(err))