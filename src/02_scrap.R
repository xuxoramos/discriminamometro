install.packages("rvest")
library(rvest)

# Create a variable holding the url information
url <- 'https://twitter.com/hashtag/puto?src=hash' 
# Parse the html code downloaded from url
twitter <- read_html(url)

## Extract tweets
# Extract raw tweets
tweets <- html_nodes(twitter, ".tweet-text")
# Remove html tags
tweets <- html_text(tweets) 
# Extract user name
users <-  html_nodes(twitter, ".js-action-profile-name b")
users <- html_text(users)
# Extract number of time tweet was favorited
favorited <- html_nodes(twitter, ".js-actionFavorite .ProfileTweet-actionCountForPresentation")
favorited <- html_text(favorited)


