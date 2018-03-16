#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(shinydashboard)

# Define UI for application that draws a histogram
ui <- fluidPage(
  dashboardPage(
    dashboardHeader(title = img(src="http://www.copred.cdmx.gob.mx/themes/base/assets/images/logos/Logo_Dependencia.png", 
                                height="47px")),
    dashboardSidebar(),
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
      helpText("Ingrese caso de discriminación"),
      textInput("caption", "Texto", "", width = '800px')

    )
  )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  output$value <- renderText({ input$caption })
}

# Run the application 
shinyApp(ui = ui, server = server)

