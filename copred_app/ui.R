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
        tabItem(tabName = "clas",
          helpText("Ingrese caso de discriminación"),
          textInput("caption", "Texto", "", width = '800px'),
          actionButton("submit", "Enter"),
          box(
            title = "Motivo de discriminación", width = NULL,
            textOutput("table")
            )
          )  
    )
    )
  )
)