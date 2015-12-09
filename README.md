# WAR of The Roses

#### *Predicting True Love on ABC's The Bachelor*

### Project Overview
Reality TV has become a staple of modern popular culture.  ABC's popular TV show The Bachelor garners millions of viewers each week.  Even under the guise of "reality" and "true love", we hypothesize that there exist underlying patterns that in general enhance a contestant's chance of winning.  To simulate this "game of love", we create a dynamic model that is updated each week of the competition that predicts contestant's chance of winning.

### Background
The Bachelor is a competition based reality TV show. Each season, about 30 women vie for a wedding proposal of a single Bachelor. Each week several women are eliminated until one contestant wins. To determine which contestants stay and which are eliminated, each week the Bachelor selects only a few contestant's to accompany him on a one-on-one or group date. At the end of the episode, there is a cocktail party where the Bachelor meets with any contestants who were not given a date during the episode. Finally, the episode closes with a rose ceremony where the Bachelor chooses who will proceed to the next episode by extending to them a rose.

### Objective
We analyze underlying features of all winning and losing contestants on the The Bachelor. Using these data, we build a statistical model to predict week-by-week success on the TV show.

# Contents
----------

### Data Scraping

#### *Twitter*
- We show how we scraped twitter to get all tweets per contestant per episode of The Bachelor.

#### *Wikipedia*
- We gather each contestant's name, age, and hometown per season according to data on Wikipedia. Additionally, for each season we gather how many group dates, one-on-one dates, and group date roses a contestant received.

### Exploratory Data Analysis / Cleaning Data

#### *Twitter Sentiment*
- We analze each tweet per contestant per episode, and use a text processing API to determine each tweet's probability of being positive. We then formulate an overall contestant positivity index per episode.

#### *Professions*
- We cluster each contestant's profession according to the [International Standard Classification of Occupations](http://www.ilo.org/public/english/bureau/stat/isco/) (ISCO) using a text analysis of the Wikipedia data.

#### *Hometowns*
- We compute the geographic distance between each contestant's hometown and the bachelor's hometown using the GeoPy library. Additionally, we cluster each contestant's hometown according to [FCC Economic Area Groupings] (http://transition.fcc.gov/oet/info/maps/areas/)

#### *Photographs - Principle Component Analysis*

### Classification / Prediction

