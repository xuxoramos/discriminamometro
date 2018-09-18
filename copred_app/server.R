#Shiny copred server

library(shiny)
library(tidyverse)
library(stringi)
library(stringr)
library(stopwords)
library(tidytext)
library(tm)
library(randomForest)


server <- function(input, output) {

  pre <- eventReactive(input$submit, {
    
    ora <- isolate(input$caption)
  
    oras <- ora %>% data.frame()
    
    names(oras) <- c("text")
    
    tew <- oras %>%
      mutate(tweet_text = gsub("@\\w+ *", "", text),
             tweet_text = tweet_text %>% 
               stri_trans_general(id = "Latin-ASCII")) %>% 
      unnest_tokens(word, tweet_text) %>% 
      right_join(palabras) %>% 
      # unique() %>% 
      mutate(unos = 1) %>% 
      spread(word,unos, fill = 0) %>% 
      inner_join(oras)
    if(nrow(tew)==0){
      return("No se encontró motivo")
    }else{
      return(predict(clasif, newdata=tew[,-1]) %>% as.character())
      # return(oras)
    }

  })
  output$table <- renderText({
    if(pre() == "genero"){
      "Género"
    }else if (pre() == "ideologia"){
      "Ideología"
    }else if (pre() == "orientacion"){
      "Orientación"
    }else if (pre() == "discapacidad"){
      "Discapacidad"
    }else if (pre() == "apariencia"){
      "Apariencia"
    }else if (pre() == "edad"){
      "Edad"
    }else{
      pre() 
    }
    })
}



