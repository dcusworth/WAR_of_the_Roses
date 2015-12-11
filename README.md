# WAR of The Roses

#### *Predicting True Love on ABC's The Bachelor*

### Project Overview
Reality TV has become a staple of modern popular culture.  ABC's popular TV show The Bachelor garners millions of viewers each week.  Even under the guise of "reality" and "true love", we hypothesize that there exist underlying patterns that in general enhance a contestant's chance of winning.  To simulate this "game of love", we create a dynamic model that is updated each week of the competition that predicts contestant's chance of winning.

### Background
The Bachelor is a competition based reality TV show. Each season, about 30 women vie for a wedding proposal of a single Bachelor. Each week several women are eliminated until one contestant wins. To determine which contestants stay and which are eliminated, each week the Bachelor selects only a few contestant's to accompany him on a one-on-one or group date. At the end of the episode, there is a cocktail party where the Bachelor meets with any contestants who were not given a date during the episode. Finally, the episode closes with a rose ceremony where the Bachelor chooses who will proceed to the next episode by extending to them a rose.

### Objective
We want to answer the following questions: 1) Can we predict weekly success on the Bachelor given a host of predictor data? 2) Can we predict when a contestant is likely to be eliminated from the show? We seek to answer this question by analyzing the underlying features of all winning and losing contestants on the The Bachelor. Using these data, we build a statistical model to predict week-by-week success on the TV show.

-----
# Contents

Below we link to HTML files of each of the iPython notebooks that were used in our analyses. To get the raw iPython notebooks, switch between branches above. Each branch contains a seperate data scraping or analysis method with the associated notebook.

### Data Scraping

* #### [*Twitter*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/twitter_scrape.html)
  - We show how we scraped twitter to get all tweets per contestant per episode of The Bachelor.

* #### [*Wikipedia*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/wiki.html)
  - We gather each contestant's name, age, and hometown per season according to data on Wikipedia. Additionally, for each season we gather how many group dates, one-on-one dates, and group date roses a contestant received.

--
### Exploratory Data Analysis / Data-Cleaning

* #### [*Twitter Sentiment*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/twitter_analysis.html)
  - We analze each tweet per contestant per episode, and use a text processing API to determine each tweet's probability of being positive. We then formulate an overall contestant positivity index per episode.

* #### [*Professions*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/profession.html)
  - We cluster each contestant's profession according to the [International Standard Classification of Occupations](http://www.ilo.org/public/english/bureau/stat/isco/) (ISCO) using a text analysis of the Wikipedia data.

* #### [*Hometown Distance*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/distances.html)
  - We compute the geographic distance between each contestant's hometown and the bachelor's hometown using the GeoPy library. 

* #### [*Hometown Clustering*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/geocluster.html) 
  - We cluster each contestant's hometown according to [FCC Economic Area Groupings] (http://transition.fcc.gov/oet/info/maps/areas/)

* #### [*Photographs - Principle Component Analysis*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/pca.html)
  - We use studio photographs from seasons 13-19 of The Bachelor and run a principle component analysis (PCA) on each image. We plot the first two principle components and color them according to success on the show.

--

### Final Analysis

* #### [*Prediction of Elimination Week*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/stats_elim.html)
 - Here we use logistic and linear regression methods to predict a contestant's which week a contestant will be eliminated (or win) based on our predictor variables outlined in the Data-Cleaning section.

* #### [*Weekly Prediction of Advancing*](http://kathrynheal.github.io/MR-DC-KH-Final-Project/stats_weekly.html)
 - We fit a unique classifier to our data for each episode from seasons 13-19, using cross-validation on a testing set. We report accuracy of the classifier on our training set. We visualize the relative importance of each predictor

--
# Conclusions
 * From fitting a unique classifier to the data each week, we find a broad consistent pattern among the data - the percentage of tweets a candidate receives in the previous week’s episodes very well influences their chances of advancing the following week. These results illuminate a producer’s point of view, Reality television is just like narrative television – the star gets the most screen time. Since the producers edit with the winner in mind, it makes sense that the bulk number of tweets serves as a proxy for screen time, and relatedly, likelihood of survival.
 * We also see a correlation between the average number of tweets a contestant receives throughout the duration of the show and their rose count. This also makes sense in terms of screen time. Contestant's who receive many dates also receive a stronger share of screen time, and thus have a stronger twitter following (hating). 
 * There are two possible reasons for why our other predictors weren’t as influential. 1) The Bachelor has only been around for 19 seasons, so maybe in 2060 when we’re watching Bachelor in Space, patterns will emerge more clearly. 2) since the show is set up so the Bachelor only has eight weeks to decide who out of thirty women he would like to spend his life, perhaps his choice is just a simple random process. 
 * To make a strong case for conclusion (2), we would want to engineer our features even more to optimize their signal. For example, we currently use the first two principal components of a contestant's entire face as features. We could improve this method with more advanced deep learning image processing algorithms that would decompose specific facial features (e.g., nose, ear, hair, etc.). After optimizing our features, we can then refit a classifier each week. If the feature still provides no information in the regression, we would then be more confident that it is uninformative.



