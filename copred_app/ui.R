#Shiny copred
#ui

library(shiny)
library(shinydashboard)

# Define UI for application that draws a histogram
ui <- fluidPage(
  dashboardPage(
    dashboardHeader(title = img(src="http://www.copred.cdmx.gob.mx/themes/base/assets/images/logos/Logo_Dependencia.png", 
                                height="47px")),
    dashboardSidebar(
      sidebarMenu(
      menuItem("Información", tabName = "info", icon =  icon("list-alt")),
      menuItem("Clasificador", tabName = "clas", icon = icon("th"))
    )
    ),
    dashboardBody(
      tags$head(tags$style(HTML('
                                .skin-blue .main-header .logo {
                                background-color: #ffffff;
                                }
                                .skin-blue .main-header .logo:hover {
                                background-color: #ffffff;
                                }
                                '))),
      tags$head(tags$style(HTML('
                                .skin-blue .main-header .navbar {
                                background-color: #e82eaa;
                                }
                                .skin-blue .main-header .navbar:hover {
                                background-color: #e82eaa;
                                }
                                '))),
      tabItems(
        tabItem(tabName = "info",
                includeMarkdown("./metodologia.md")),
        tabItem(tabName = "clas",
          helpText("Ingrese caso de discriminación"),
          textInput("caption", "Texto", "", width = '800px'),
          actionButton("submit", "Enter"),
          box(
            title = "Motivo de discriminación", width = NULL,
            textOutput("table")
            ),
          box(title='¿Cómo leer este contenido?', HTML('En este apartado se muestra el resultado del análisis por cada tipo de discriminación.<br/>Se puede observar que la religión no figura entre las categorías con más incidentes en redes sociales. Sin embargo, de acuerdo a datos de COPRED, el motivo religioso es el que más se reporta <i>in situ</i>.<br/>En cada uno de los paneles a continuación, se muestra una nube de palabras a la izquierda, la cual cuenta la frecuencia de los términos buscados en todo el contenido, y a la derecha una asociación entre una palabra de interés para COPRED, y las frases que lo acompañan. La métrica en el eje de las X representa la relevancia dentro de las conversaciones de la intersección entre palabra discriminatoria identificada VS frase que co-ocurre junto con ella.'), width = 12),
          fluidRow(
                   box(
                     title = "Orientación",width = 12,
                     column(width=3, align="center",
                            img(src="word_orientacion.png", height=400)),
                     column(width=9, align="center",
                            img(src="bigramorientacion.png", height=400)))),
          fluidRow(
                   box(
                     title = "Género",width = 12,
                     column(width=3, align="center",
                            img(src="word_genero.png", height=400)),
                     column(width=9, align="center",
                            img(src="bigramgenero.png", height=400)))),
          fluidRow(
                   box(
                     title = "Apariencia",width = 12,
                     column(width=3, align="center",
                            img(src="word_apar.png", height=400)),
                     column(width=9, align="center",
                            img(src="bigramapariencia.png", height=400)))),
          fluidRow(
                   box(
                     title = "discapacidad",width = 12,
                     column(width=3, align="center",
                            img(src="word_disc.png", height=400)),
                     column(width=9, align="center",
                            img(src="bigramdiscapacidad.png", height=400)))),
          fluidRow(
                   box(
                     title = "Edad",width = 12,
                     column(width=3, align="center",
                            img(src="word_edad.png", height=400)),
                     column(width=9, align="center",
                            img(src="bigramedad.png", height=400)))),
          fluidRow(
                   box(
                     title = "Ideología",width = 12,
                     column(width=3, align="center",
                            img(src="word_ideo.png", height=400)),
                     column(width=9, align="center",
                            img(src="bigramideologia.png", height=400)))
          )
          
          )  
    )
    )
  )
)