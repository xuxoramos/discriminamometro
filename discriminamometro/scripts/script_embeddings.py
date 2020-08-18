import Discrim.Train.embeddings as emb

def embeddings():
    
    obj_emb = emb.Embeddings()
    obj_emb.descargar_archivo_fuente()
    obj_emb.transformar_dataset()
    obj_emb.generar_embeddings()
    obj_emb.enviar_embeddings_s3()

    return

if __name__== "__main__" :

    try:
    
        embeddings()
    
    # Si llega a tronar algo, cachamos el error y lo escribimos en el archivo log para saber qué fue
    except Exception as err:
        with open('script_embeddings_error.txt', 'w') as file:
            file.write(str(err))


