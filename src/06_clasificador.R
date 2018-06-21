#Script juntando todos lo tweets

library(tidyverse)
library(stringi)
library(stringr)
library(stopwords)
library(tidytext)
library(tm)
library(e1071)
library(RTextTools)
library(caret)
library(caTools)
library(rpart)
#library(rpart.plot)
library(randomForest)
library(wordcloud)

base_discr_comp <-  rbind(read_rds("discriminating-words/data/tweets/base_apariencia.RDS"),
                   read_rds("discriminating-words/data/tweets/base_discapacidad.RDS"),
                   read_rds("discriminating-words/data/tweets/base_edad.RDS"),
                   read_rds("discriminating-words/data/tweets/base_genero.RDS"),
                   read_rds("discriminating-words/data/tweets/base_ideologia.RDS"),
                   read_rds("discriminating-words/data/tweets/base_orientacion.RDS"),
                   read_rds("discriminating-words/data/tweets/base_religion.RDS"),
                   read_rds("discriminating-words/data2/tweets/base_apariencia.RDS"),
                   read_rds("discriminating-words/data2/tweets/base_discapacidad.RDS"),
                   read_rds("discriminating-words/data2/tweets/base_edad.RDS"),
                   read_rds("discriminating-words/data2/tweets/base_genero.RDS"),
                   read_rds("discriminating-words/data2/tweets/base_ideologia.RDS"),
                   read_rds("discriminating-words/data2/tweets/base_orientacion.RDS"),
                   read_rds("discriminating-words/data2/tweets/base_religion.RDS")) %>% 
  select(text,tipo,motivo) %>% 
  mutate(folio = 1:nrow(.),
         text = stri_trans_general(text, id = "Latin-ASCII") %>% 
           tolower(),
         motivo = ifelse(motivo == "ideoligia", "ideologia", motivo)) %>% 
  rename(class = motivo) %>% 
  unique() 

base_discr_comp %>% 
  group_by(class) %>% 
  tally()

orientacion <- base_discr_comp %>% 
  filter(class == "orientacion") %>% 
  .$text %>% 
  sample(size = 10000, replace = T)

discapacidad <- base_discr_comp %>% 
  filter(class == "discapacidad") %>% 
  .$text %>% 
  sample(size = 20000, replace = T)

apariencia <- base_discr_comp %>% 
  filter(class == "apariencia") %>% 
  .$text %>% 
  sample(size = 20000, replace = T)

genero <- base_discr_comp %>% 
  filter(class == "genero") %>% 
  .$text %>% 
  sample(size = 30000, replace = T)

ideologia <- base_discr_comp %>% 
  filter(class == "ideologia") %>% 
  .$text %>% 
  sample(size = 20000, replace = T)

edad <- base_discr_comp %>% 
  filter(class == "edad") %>% 
  .$text %>% 
  sample(size = 10000, replace = T)

religion <- base_discr_comp %>% 
  filter(class == "religion") %>% 
  .$text %>% 
  sample(size = 10000, replace = T)

# base_discr <- base_discr_comp %>% 
#   select(class, text) %>% 
#   filter(class %in% c("apariencia", "genero", "ideologia")) %>% 
#   rbind(data.frame(class = "orientacion", text = orientacion),
#         data.frame(class = "discapacidad", text = discapacidad))

base_discr <- rbind(data.frame(class = "orientacion", text = orientacion),
                    data.frame(class = "discapacidad", text = discapacidad),
                    data.frame(class = "apariencia", text = apariencia),
                    data.frame(class = "edad", text = edad),
                    data.frame(class = "genero", text = genero),
                    data.frame(class = "ideologia", text = ideologia))
base_discr %>% 
  group_by(class) %>% 
  tally()

palabras <- read_csv("discriminating-words/docs/catalogo_palabras.csv")

tweets_tokens <- base_discr %>% 
  select(class, text) %>% 
  mutate(tweet_text = gsub("@\\w+ *", "", text),
         tweet_text = tweet_text %>% 
           stri_trans_general(id = "Latin-ASCII")) %>% 
  unnest_tokens(word, tweet_text) %>%
  inner_join(palabras)

#write.csv(base_discr, "discriminating-words/data/tweets_api.csv")

datos_categ <- tweets_tokens %>% 
  unique() %>% 
  mutate(unos = 1) %>% 
  spread(word, unos, fill = 0)

#nb class separando entrenamoento y prueba

set.seed(1)
df <- datos_categ[sample(nrow(datos_categ)), ]
glimpse(df)

df$class <- as.factor(df$class)
## 75% of the sample size
smp_size <- floor(0.75 * nrow(datos_categ))

## set the seed to make your partition reproducible
set.seed(123)
train_ind <- sample(seq_len(nrow(df)), size = smp_size)

train <- df[train_ind, ]
test <- df[-train_ind, ]

df.train <- train
df.test <- test

trainNB <- df.train[,3:115]
testNB <- df.test[,3:115]

system.time( classifier <- naiveBayes(trainNB, df.train$class, laplace = 0) )

system.time( pred <- predict(classifier, newdata=testNB) )

table("Predictions"= pred,  "Actual" = df.test$class )
conf.mat <- confusionMatrix(pred, df.test$class)

conf.mat

#clasificador con la base de datos completa

classifier_com <- naiveBayes(df[,3:115], df$class, laplace = 0) 

#tweet discriminador 

ora <- "pinche puto puto puto"
oras <- ora %>% data.frame()

names(oras) <- c("text")

tew <- oras %>% 
  mutate(tweet_text = gsub("@\\w+ *", "", text),
         tweet_text = tweet_text %>% 
           stri_trans_general(id = "Latin-ASCII")) %>% 
  unnest_tokens(word, tweet_text) %>%
  inner_join(palabras) %>% 
  unique() %>% 
  mutate(unos = 1) %>% 
  spread(word,unos, fill = 0)

pred <- predict(classifier_com, newdata=tew[,-1])
pred

#guardando el clasificador

saveRDS(object = classifier_com, "discriminating-words/copred_app/base_clasif.rds")

# nubes de palabras -------------------------------------------------------

stop_words <- read_csv("discriminating-words/docs/stopwords_espanol.csv")

frec_ideologia <- base_discr %>% 
  select(class, text) %>% 
  filter(class == "ideologia") %>% 
  mutate(tweet_text = gsub("@\\w+ *", "", text),
         tweet_text = tweet_text %>% 
           stri_trans_general(id = "Latin-ASCII")) %>% 
  unnest_tokens(word, tweet_text) %>%
  filter(!word %in% c(stop_words$text, "rt", "https", "t.co","jajajajaja","tw","i0s79pdyt","ah",
                      "vas", "ay","dije","pri", "panistas", "amloyapactoconelpr", "aseguro",
                      "rico", "detene", "amloyapactoconelpri", "zts2sdmw", "3dtwpwlj7g",
                      "rzyekxumxd", "zffhjvtkvn", "xjdyn7zis1", "g5k33s6vni",
                      "aguilas", "2016", "18", "julio", "aho", "morena", "kgumps8esb", "brlzw",
                      "5585680050")) %>% 
  group_by(word) %>% 
  tally() %>% 
  ungroup() %>% 
  mutate(n = ifelse(word %in% c("indio", "pejezoembie", "voto", "unam"), n * 5, n))

#saveRDS(object = frec_orientacion, file = "discriminating-words/copred_app/frac_nubes/orientacion.rds")

set.seed(1234)
wordcloud(words = frec_ideologia$word, freq = frec_ideologia$n, min.freq = 10,
          max.words=120, random.order=FALSE, rot.per=0.25, 
          colors=brewer.pal(8, "Dark2"), scale = c(2,.5))

