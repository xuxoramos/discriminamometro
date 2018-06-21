#script lectura de tweets con geocode
# Fetch TWs
library(twitteR)

# llaves
tw_api_key <- 'QOe4KhUucn8hRP9pJ2q2QYksnn'
tw_api_secret <- 'HYiwanxtHDuaew2mnEXgCVhVxD3zEEZo77K8ihJDZhqPBrmhdoo'
access_token <- '777720164011773953-10EFKORqQpsdFsCnfsTY4P7iko6SkIWW'
access_secret <- 'c8xKppCWwpU2veAuTW6bGMfSoSlkA1GnlD9Rh3isDbyu99'

setup_twitter_oauth(tw_api_key, tw_api_secret, access_token, access_secret)


# Género ------------------------------------------------------------------

## Vieja loca

tw <- twitteR::searchTwitter('vieja+loca', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

vieja_loca <- twitteR::twListToDF(tw)

saveRDS(vieja_loca, "discriminating-words/data2/tweets/genero/vieja_loca_geo.RDS")

##mamá luchona

tw <- twitteR::searchTwitter('mama+luchona', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

mama_luchona<- twitteR::twListToDF(tw)

saveRDS(mama_luchona, "discriminating-words/data2/tweets/genero/mama_luchona.RDS")

#como niña

tw <- twitteR::searchTwitter('como niña', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

como_nina <- twitteR::twListToDF(tw)

saveRDS(como_nina, "discriminating-words/data2/tweets/genero/como_nina.RDS")

##es de niña

tw <- twitteR::searchTwitter('es de niña', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

es_de_nina <- twitteR::twListToDF(tw)

saveRDS(es_de_nina, "discriminating-words/data2/tweets/genero/es_de_nina.RDS")

#como los hombres

tw <- twitteR::searchTwitter('como los hombres', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

como_hombre <- twitteR::twListToDF(tw)

saveRDS(como_hombre, "discriminating-words/data2/tweets/genero/como_hombre.RDS")

#para qué tienes hijos

tw <- twitteR::searchTwitter('para+que+tienes+hijos', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

tienes_hijos <- twitteR::twListToDF(tw)

saveRDS(tienes_hijos, "discriminating-words/data2/tweets/genero/tienes_hijos.RDS")

#veja pendeja

tw <- twitteR::searchTwitter('vieja pendeja', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

veja_pendeja <- twitteR::twListToDF(tw)

saveRDS(veja_pendeja, "discriminating-words/data2/tweets/genero/veja_pendeja.RDS")

#discriminacion embarazada

tw <- twitteR::searchTwitter('discriminacion embarazada', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

discriminacion_embarazada <- twitteR::twListToDF(tw)

saveRDS(discriminacion_embarazada, "discriminating-words/data2/tweets/genero/discriminacion_embarazada.RDS")

#discriminacion mujeres

tw <- twitteR::searchTwitter('discriminacion mujeres', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

discriminacion_mujeres <- twitteR::twListToDF(tw)

saveRDS(discriminacion_mujeres, "discriminating-words/data2/tweets/genero/discriminacion_mujeres.RDS")

## feminazi

tw <- twitteR::searchTwitter('feminazi', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

feminazi <- twitteR::twListToDF(tw)

saveRDS(feminazi, "discriminating-words/data2/tweets/genero/feminazi.RDS")

# orientación/identidad sexual --------------------------------------------

## pinche lesbiana

tw <- twitteR::searchTwitter('pinche lesbiana', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pinche_lesbiana <- twitteR::twListToDF(tw)

saveRDS(pinche_lesbiana, "discriminating-words/data2/tweets/orientacion/pinche_lesbiana.RDS")

## lesbiana

tw <- twitteR::searchTwitter('lesbiana', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

lesbiana <- twitteR::twListToDF(tw)

saveRDS(lesbiana, "discriminating-words/data2/tweets/orientacion/lesbiana.RDS")

##Le gusta el arroz con popote

tw <- twitteR::searchTwitter('arroz con popote', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

arroz_popote <- twitteR::twListToDF(tw)

saveRDS(arroz_popote, "discriminating-words/data2/tweets/orientacion/arroz_popote.RDS")

##puñal

tw <- twitteR::searchTwitter('puñal', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

punial <- twitteR::twListToDF(tw)

saveRDS(punial, "discriminating-words/data2/tweets/orientacion/punial.RDS")

##machorra

tw <- twitteR::searchTwitter('machorra', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

machorra <- twitteR::twListToDF(tw)

saveRDS(machorra, "discriminating-words/data2/tweets/orientacion/machorra.RDS")

## Pinche maricon

tw <- twitteR::searchTwitter('Pinche maricon', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pinche_maricon <- twitteR::twListToDF(tw)

saveRDS(pinche_maricon, "discriminating-words/data2/tweets/orientacion/pinche_maricon.RDS")

##pinche puto

tw <- twitteR::searchTwitter('pinche puto', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pinche_puto <- twitteR::twListToDF(tw)

saveRDS(pinche_puto, "discriminating-words/data2/tweets/orientacion/pinche_puto.RDS")

##joto

tw <- twitteR::searchTwitter('joto', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

joto <- twitteR::twListToDF(tw)

saveRDS(joto, "discriminating-words/data2/tweets/orientacion/joto.RDS")

##lencha 

tw <- twitteR::searchTwitter('lencha', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

lencha <- twitteR::twListToDF(tw)

saveRDS(lencha, "discriminating-words/data2/tweets/orientacion/lencha.RDS")










# Ideología política ------------------------------------------------------

##chairo

tw <- twitteR::searchTwitter('chairo', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

chairo <- twitteR::twListToDF(tw)

saveRDS(chairo, "discriminating-words/data2/tweets/ideologia_politica/chairo.RDS")


##derechairo

tw <- twitteR::searchTwitter('derechairo', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

derechairo <- twitteR::twListToDF(tw)

saveRDS(derechairo, "discriminating-words/data2/tweets/ideologia_politica/derechairo.RDS")

##feminazi

tw <- twitteR::searchTwitter('feminazi', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

feminazi <- twitteR::twListToDF(tw)

saveRDS(feminazi, "discriminating-words/data2/tweets/ideologia_politica/feminazi.RDS")

##
# Apariencia (tatuajes, pobreza, condición económica o social) ------------

## Naco

tw <- twitteR::searchTwitter('naco', 
                             n = 5000, 
                             retryOnRateLimit = 500,
                             geocode='19.382099,-99.136102,90km')

naco <- twitteR::twListToDF(tw)

saveRDS(naco, "discriminating-words/data2/tweets/apariencia/naco.RDS")

## jodido

tw <- twitteR::searchTwitter('jodido', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

jodido <- twitteR::twListToDF(tw)

saveRDS(jodido, "discriminating-words/data2/tweets/apariencia/jodido.RDS")

## iztapalacra

tw <- twitteR::searchTwitter('iztapalacra', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

iztapalacra <- twitteR::twListToDF(tw)

saveRDS(iztapalacra, "discriminating-words/data2/tweets/apariencia/iztapalacra.RDS")

## chacha

tw <- twitteR::searchTwitter('chacha', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

chacha <- twitteR::twListToDF(tw)

saveRDS(chacha, "discriminating-words/data2/tweets/apariencia/chacha.RDS")

## pinche_fresa

tw <- twitteR::searchTwitter('pinche fresa', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pinche_fresa <- twitteR::twListToDF(tw)

saveRDS(pinche_fresa, "discriminating-words/data2/tweets/apariencia/pinche_fresa.RDS")

## pinche negro

tw <- twitteR::searchTwitter('pinche negro', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pinche_negro <- twitteR::twListToDF(tw)

saveRDS(pinche_negro, "discriminating-words/data2/tweets/apariencia/pinche_negro.RDS")

## pinche gordo

tw <- twitteR::searchTwitter('pinche gordo', 
                             n = 5000, 
                             retryOnRateLimit = 500,
                             geocode='19.382099,-99.136102,90km')

pinche_gordo<- twitteR::twListToDF(tw)

saveRDS(pinche_gordo, "discriminating-words/data2/tweets/apariencia/pinche_gordo.RDS")

## pinche indio

tw <- twitteR::searchTwitter('pinche indio', 
                             n = 5000, 
                             retryOnRateLimit = 500,
                             geocode='19.382099,-99.136102,90km')

pinche_indio<- twitteR::twListToDF(tw)

saveRDS(indio, "discriminating-words/data2/tweets/apariencia/pinche_indio.RDS")

## pinche pobre

tw <- twitteR::searchTwitter('pinche pobre', 
                             n = 5000, 
                             retryOnRateLimit = 500,
                             geocode='19.382099,-99.136102,90km')

pinche_pobre<- twitteR::twListToDF(tw)

saveRDS(pinche_pobre, "discriminating-words/data2/tweets/apariencia/pinche_pobre.RDS")


## guerito

tw <- twitteR::searchTwitter('guerito', 
                             n = 5000, 
                             retryOnRateLimit = 500,
                             geocode='19.382099,-99.136102,90km')

guerito <- twitteR::twListToDF(tw)

saveRDS(guerito, "discriminating-words/data2/tweets/apariencia/guerito.RDS")

# religion ----------------------------------------------------------------

## pinche judio

tw <- twitteR::searchTwitter('pinche judio', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pinche_judio <- twitteR::twListToDF(tw)

saveRDS(pinche_judio, "discriminating-words/data2/tweets/religion/pinche_judio_geo.RDS")

## testiculos de jehova
tw <- twitteR::searchTwitter('testiculos de jehova', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

testiculos_jehova <- twitteR::twListToDF(tw)

saveRDS(testiculos_jehova, "discriminating-words/data2/tweets/religion/testiculos_jehova.RDS")

##testigos de Jehova

tw <- twitteR::searchTwitter('testigos de Jehova', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

testigos_jehova <- twitteR::twListToDF(tw)

saveRDS(testigos_jehova, "discriminating-words/data2/tweets/religion/testigos_jehova.RDS")

##religioso pendejo

tw <- twitteR::searchTwitter('religioso pendejo', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

religioso_pendejo <- twitteR::twListToDF(tw)

saveRDS(religioso_pendejo, "discriminating-words/data2/tweets/religion/religioso_pendejo.RDS")



# edad --------------------------------------------------------------------

## pinche viejo

tw <- twitteR::searchTwitter('pinche viejo', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pinche_viejo<- twitteR::twListToDF(tw)

saveRDS(pinche_viejo, "discriminating-words/data2/tweets/edad/pinche_vieji.RDS")

## pinche ninio

tw <- twitteR::searchTwitter('pinche nino', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pinche_ninio<- twitteR::twListToDF(tw)

saveRDS(pinche_ninio, "discriminating-words/data2/tweets/edad/pinche_ninio.RDS")

## pareces_nino_chiquito

tw <- twitteR::searchTwitter('pareces nino chiquito', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

pareces_nino_chiquito<- twitteR::twListToDF(tw)

saveRDS(pareces_nino_chiquito, "discriminating-words/data2/tweets/edad/pareces_nino_chiquito.RDS")

##es_chavo

tw <- twitteR::searchTwitter('es chavo', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

es_chavo <- twitteR::twListToDF(tw)

saveRDS(es_chavo, "discriminating-words/data2/tweets/edad/es_chavo.RDS")

##chavoruco 

tw <- twitteR::searchTwitter('chavorruco', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

tw_2 <- twitteR::searchTwitter('chavoruco', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

chavoruco <- rbind(twitteR::twListToDF(tw), twitteR::twListToDF(tw_2))

saveRDS(chavoruco, "discriminating-words/data2/tweets/edad/chavoruco.RDS")

##nini

tw <- twitteR::searchTwitter('NINI', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

nini <- twitteR::twListToDF(tw)

saveRDS(nini, "discriminating-words/data2/tweets/edad/nini.RDS")


# discapacidad ------------------------------------------------------------

##ciego
tw <- twitteR::searchTwitter('ciego', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

ciego <- twitteR::twListToDF(tw)

saveRDS(ciego, "discriminating-words/data2/tweets/discapacidad/ciego.RDS")

##cojo
tw <- twitteR::searchTwitter('cojo', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

cojo <- twitteR::twListToDF(tw)

saveRDS(cojo, "discriminating-words/data2/tweets/discapacidad/cojo.RDS")

##discapacitado

tw <- twitteR::searchTwitter('discapacitado', 
                             n = 10000, 
                             retryOnRateLimit = 1000,
                             geocode='19.382099,-99.136102,90km')

discapacitado <- twitteR::twListToDF(tw)

saveRDS(discapacitado, "discriminating-words/data2/tweets/discapacidad/discapacitado.RDS")



