# ada-2023-project-vivalavada
ada-2023-project-vivalavada created by GitHub Classroom

## Cheers to Change: Exploring Temporal and Spatial Dynamics in Beer Preferences

## Abstract

We propose in this study to analyze what are the beer preferences of different locations, and how their evaluation and spreading over time reflect the interconnection between countries. Our definition of "beer preference" for a location encompasses the most consumed beer styles, those with the highest ratings, as well as the brewery locations that are both the most consumed and highest rated. Additionally, we explore global preferences to provide a comprehensive understanding of the dynamics in beer consumption and evaluation worldwide. In the end, our objective is to explore whether countries that are close together, either geographically or socio-economically, exhibit similarity in terms of beer preferences, and how these similarities evolve.

You can check our data story is given in the [link](https://hadriensevel.github.io/vivalavada/).

## Research Questions

1. According to our above-given beer preference definitions, what are the different preferences and how do beer consumption habits change over the years for each location?

2. How long does a country have the same preference? Do preferences of the different locations around the globe spread to other countries?

3. Apart from the local beer preferences in separate locations, what is the global beer preference, and how does it change over time?

4. Are the beer preferences of some locations considerably similar to that of some other locations? If yes, does the geographical distance and wealth difference between the locations play an important role in this? Furthermore, how do global similarities in beer preferences evolve?

## Additional Datasets 

1. [World Population Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset): This dataset gives us the population of each country by year, which is used to calculate the percentage of population of each country that have accounts in either of the websites. Population also gives us a further parameter to analyze the trends of each country. We merged our existing datasets of users, ratings, and breweries with the population dataset based on the attribute of location. We considered the year 2010 by reading the populations, which is a suitable year for our time range, from 2006 to 2017.

2. [Us State Population Dataset](https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html): We use this dataset with the same goal as the previous one but for distinct states in the United States. Again, consider only the data from 2010 to be consistent with the country years.

4.  [US State Wealth Dataset](https://ssti.org/blog/useful-stats-capita-gross-state-product-1998-2018))
   This dataset gives the GDP per capita for each state in 2018. It also gives the percentage change over a 10 period time. Therefore, we can apply that change to see the GDP per capita for each US state in 2008 which falls into our year range of interest. 

5. [Country Wealth dataset](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?end=2008&start=2007)
   This dataset gives the GDP per capita for each country for each year in terms of 2012 US dollars. To combine with the states dataset, we will only look at the year 2008 only, and convert the value of the 2012 US dollar to its corresponding value in 2008 so that the values are comparable with the previous dataset. We shall use an [inflation calculator](https://www.bls.gov/data/inflation_calculator.htm) to make the adjustment.
   

## Methods 

### *Step 1: Preprocessing*

##### *1. Merging*

We were given data from two different websites - RateBeer and BeerAdvocate. In order not to waste any data, we merged the two datasets. The exact method followed by merging is given with comments in the notebook. To summarize, we removed the intersection of users and ratings from the data of individual websites to avoid duplicates using the matched dataset. We then added the intersection back again. Furthermore, we mapped every beer style and every beer_id, user_id, and brewery_id in the matched data to its RateBeer version.

##### *2. Normalizing the Data*

We standardized the ratings and each aspect of the ratings (appearance, palate, taste, and aroma) by subtracting the mean of the year for the given website and then dividing by the standard deviation of that year. This way, biases coming from different levels of ratings from the two websites and biases of rating inflations or deflations between different years are eliminated. As an end-effect, all the ratings in the merged dataset are directly comparable to each other.

##### *3. Filtering the Data*

We visualized the data and removed unreliable data points. For example, there were a few beers with higher than 50% alcohol percentages or users more than 20,000 ratings. Such datapoints are eliminated for more reliable future analysis.

##### *4. Reading in additional population datasets*

Our data consisted of users with locations and breweries with locations. The locations were either countries or states within the United States, so we combined two separate datasets on countries and US state populations to create a general population data frame. 

##### *5. Selecting Year Range and Locations*

In the notebook, we analyzed for which years we have enough amount of data for analysis. Moreover, for each location, we measured the number of distinct users divided by the total population and we only included locations where the percentage of users is high enough. We also put a condition that for each year of interest, the valid locations should have at least a predefined number of ratings. The final sets of time range and location set are given below: 

**Time range:** years from 2006 to 2017, including 2006 and 2017.

**Location set:** All states of U.S. except South Dakota (49 states), Iceland, Denmark, Canada, Norway, Sweden, Belgium, New Zealand, Ireland, Finland, Scotland, Australia, Netherlands, Luxembourg, England, Poland, Croatia, Northern Ireland, Spain, Italy, Germany, France and Brazil.

We regard each state of U.S. as a separate location rather than naming them all U.S.A. This is because most of the data comes from different states of U.S and it is a much bigger country than the other countries in our list so reducing them all to a single name and location would waste too much data. Because of this decision, we call this a "location set" rather than a "country set".

### *Step 2: Visualizations and Initial Analysis*

We plotted the locations we filtered out on a map, using the latitude and longitude coordinates from open street maps for each coordinate. We also plotted the brewery locations on a heatmap using a similar process. We then implemented some initial methods to find the most popular or highest-rated beer styles/beer producers. We also fitted a basic OLS model to see the coefficients of each beer aspect (taste, appearance, etc.) to the overall rating. Lastly, we have found the Pearson correlation coefficient. and corresponding p_value between the overall rating and alcohol by volume. Although basic, these analyses allowed us to better understand our data.


### *Step 3: Answering the research questions*
 
#### *Question 1*

We extracted the most popular (in quantity) beer style and beer production place (brewery location) for each location for each year by looking at the total number of ratings. We divide the number of ratings by the total number of ratings for that location to get a comparable result. Furthermore, we determined that for a beer style or brewery location to be considered a preference for a location, it must be at least as popular (in terms of its percentage in the total number of ratings) as its overall global popularity. As a result, we excluded those that did not meet this criterion from our analysis.

For investigating the beer styles and brewery locations with the highest ratings, we take the average of the ratings and compare them, however, we also put a threshold on the number of ratings to be satisfied for being considered in this analysis. We standardize the ratings using location mean and standard deviation to get a comparable result. 

#### *Question 2*

We took the values found in Question 1 and visualized the spread and duration of preferences using colors in the world map.

#### *Question 3* 

To find the global preferences, we again used the values found in Question 1. For each location, we assigned points to their top 10 favorite beer styles or brewery locations. The points are assigned by mimicking the rating system used in the Eurovision Song Contest: 12 points for the most preferred beer style or brewery location, 10 points for the second most preferred one, 8 points for the third most preferred one, and so on. Moreover, since we have too many U.S. states, to find a more realistic and fair global preference we treated the whole U.S. as a single location. By applying this process, we found the most popular and highest-rated beer styles and brewery locations for each year globally.

#### *Question 4*

We defined similarity metrics between beer preferences as follows:

- For beer styles, we use the Jaccard similarity metric. We extracted the top 3 beer style preferences for each location each year. The beer style preference similarity of the two locations is calculated between their corresponding beer style preference sets of size 3.

For the brewery locations, we use the inverse of the geographical distance between the preferred brewery locations of the two locations to define how 'similar' their preferred brewery locations are.

To assess the effect of geographical distance and wealth, we computed the 15 most similar and most different locations for those two facets. For location, we used the geographical distance between each location pair. For wealth, we used the difference in GDP per capita so that population and country size would not play a factor. Then, using the metrics for similarities defined above, for each location, we found the mean pairwise preference similarity of it with the 15 most similar locations and the 15 most different locations to it. Furthermore, we applied t-tests to distributions of the mean similarity of the closest locations and the mean similarity of the farthest locations to assess their difference. Finally, we calculated a single similarity score for each pair of locations for each year and calculated the Pearson correlation coefficient between the beer preference similarity and GDP per capita difference or geographical distance.

To find the global similarity, we calculated the similarity between each two pairs of locations for each year and took the mean of the pairwise similarity for all pairs.


### *Step 4: Data story with visualizations*

Using all the findings we obtained by answering the research questions, we created a data story enriched by visualizations such as interactive plots. 


## Planning

1.12:
 - Extraction of local preferences
 - Similarity definition and calculating pairwise similarities between locations

8.12: 
 - Extraction of global preferences
 - Finding the 15 closest and 15 farthest countries and calculating respective similarities.
 - Calculating global similarities

15.12: 
 - Representing the local preferences on a map to extract duration or spread information
 - Perform the t-tests and calculate the Pearson coefficients

22.12:
 - Finish the datastory
 - Finish the visualization


## Team organization

Tugba and Yagiz: Definition of beer preferences and creation of the dataframes. Definition of beer trends.

Hadrien: Website and interactive figures and maps.

Rishi and Iris: Similarity definition, dataframes of similarities and corresponding graphs.
