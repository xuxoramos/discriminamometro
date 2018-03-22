#script reporte hechos copred

rm(list = ls())

#library(xlsx)
library(tidyverse)
library(magrittr)
library(tidytext)
library(tm)
library(stringi)
library(reshape2)
library(wordcloud)
library(topicmodels)

#base_reportes_raw <- readxl::read_xlsx("data/RPORTE HECHOS COPRED (ok).xlsx", sheet = 1)

base_reportes_raw <- read_csv("data/hechos.csv")

glimpse(base_reportes_raw)

#seleccion de variables que nos interesan
base_reportes <- base_reportes_raw %>% 
  select(id, tipo_actor_id, tipo_actor, fecha_ingreso,
         fecha_ultima_accion, tipo_intervencion, derecho_vulnerado,
         estatus, medio_ingreso, tipo_gestion_id, lugar_hechos,
         dele_mpio, genero, ocupacion, edad_primer_contacto, grupo_pobla,
         tipo_discri, motivo_discriminacion_id, motivo_dicriminacion, 
         narracion_hechos) %>% 
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
                                  "asi", "ser", "anos", "hace")) %>% 
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

#TF - IDF
base_reportes %>% 
  group_by(motivo_dicriminacion) %>% 
  summarise(texto = paste0(narracion_hechos, collapse = "")) %>% 
  mutate(tam = stri_length(texto)) %>% 
  select(motivo_dicriminacion, tam) %>% 
  View()

base_nar_motivo <- base_reportes %>% 
  group_by(motivo_dicriminacion) %>% 
  summarise(texto = paste0(narracion_hechos, collapse = "")) %>% 
  ungroup() %>% 
  unnest_tokens(word, texto) %>% 
  mutate(word = stri_trans_general(word, id = "Latin-ASCII")) %>% 
  anti_join(stop_words) %>% 
  count(word, motivo_dicriminacion) %>% 
  na.omit() 

base_nar_motivo %>% 
  filter(word != 'na') %>% 
  bind_tf_idf(word, motivo_dicriminacion, n) %>% 
  acast(word ~ motivo_dicriminacion,
        value.var = 'tf_idf',
        fill = 0) %>% 
  comparison.cloud(max.words = 300, title.size = 1)

#topic m  odeling

lda_base <- base_nar_motivo %>% 
  mutate(num = str_replace(word, '[^[:alpha:]]+',"")) %>% 
  filter(num != "") %>% 
  cast_dtm(motivo_dicriminacion, word, n) %>% 
  topicmodels::LDA(k = 5, control = list(seed = 1234))


