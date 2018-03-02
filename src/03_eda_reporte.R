#script reporte hechos copred

rm(list = ls())

library(xlsx)
library(tidyverse)
library(magrittr)
library(tidytext)
library(tm)
library(stringi)

base_reportes_raw <- readxl::read_xlsx("data/RPORTE HECHOS COPRED (ok).xlsx", 
                                   sheet = 1)

glimpse(base_reportes)

summary(base_reportes)

#seleccion de variables que nos interesan
base_reportes <- base_reportes_raw %>% 
  select(id, tipo_actor_id, tipo_actor, fecha_ingreso,
         fecha_ultima_accion, tipo_intervencion, derecho_vulnerado,
         estatus, medio_ingreso, tipo_gestion_id, lugar_hechos,
         dele_mpio, genero, ocupacion, edad_primer_contacto, grupo_pobla,
         tipo_discri, motivo_discriminacion_id, motivo_dicriminacion) %>% 
  mutate_if(is.character, as.factor)

glimpse(base_reportes)

summary(base_reportes)

comentarios <- base_reportes_raw %>% 
  select(narracion_hechos) %>% 
  na.omit() %>% 
  mutate(id = row_number())

palabras <- comentarios %>% 
  unnest_tokens(word, narracion_hechos)

stop_words <- data.frame(word = c(tm::stopwords(kind = "es"), "c", "dia", 2017,
                                  "hacia", "00", "dos", "vez", "ano", "obstante",
                                  "asi", "ser")) %>% 
  mutate(word = stri_trans_general(word, id = "Latin-ASCII"))

tidy_words <- palabras %>%
  mutate(word = stri_trans_general(word, id = "Latin-ASCII") %>% 
           tolower()) %>% 
  anti_join(stop_words)

n_pal <- tidy_words %>% 
  count(word, sort = T)

n_pal %>%
  filter(n > 1000) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip()
