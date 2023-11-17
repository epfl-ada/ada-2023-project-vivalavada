# ada-2023-project-vivalavada
ada-2023-project-vivalavada created by GitHub Classroom

## Question: How do beer trends evolve with time and location? 


## Abstract 

We propose in this study to analyze how different regions' beer preferences change with regard to the distance between neighboring places over time. As technology and transportation has increased, for example, we want to see if Canadians may drink more beer from the United States over time because of their relative proximity as opposed to drinking more beer from France since France is further away. We shall investigate many different metrics to check the popularity of different styles of beer over time, such as the styles that are most consumed, the styles with the highest ratings, and the number of breweries that primarily produce a certain style. Our motivation is to see whether countries that are close together geographically have become more interconnected over time through the lens of beer, and what factors make certain styles popular. 

## Research Questions

1. How does the popularity and style rating for each type of beer change over the years for a specific location? For each region of interest, we want to look at the distribution of beers they are consuming and the beers they are giving the highest ratings to, and see if that is changing with time. 

2. Overall, what styles of beer are rated the most, and which get the highest rating? Is there a specific location that produces higher beer scores for each brewery?

3. What factors in the beer between taste, aroma, and palate contribute most to a higher rating value? 

4. Do some countries share the same trends of other countries in terms of the style of beers they are consuming, and if so, we would like to look at the reason behind this. We would like to see if there is a correlation between distance of two countries and their beer trends, differences in wealth, or differences in language. 




## Additional Datasets 

1. [Country Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset): We use this dataset to get the percentage of users. Population also gives us a further parameter to analyze the trends of each country. We merged our existing datasets of users, ratings, and breweries with the population dataset based on the attribute of location. A lot of users were from countries outside the US, while others were from states inside the US. We used the latest population year that they gave us (*which was 2022*)

2. [Us State Population Dataset](https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html): We use this dataset with the same goal as the previous one, but for distinct states in the United States. Multiple years were given, but we chose 2010 to be consistent with the country years as well.

3. [Languages Dataset](https://resourcewatch.org/data/explore/soc_071_world_languages?section=Discover&selectedCollection=&zoom=3&lat=0&lng=0&pitch=0&bearing=0&basemap=dark&labels=light&layers=%5B%7B%22dataset%22%3A%2220662342-dcdd-4a42-9f58-bcc80217de71%22%2C%22opacity%22%3A1%2C%22layer%22%3A%22f2d76e6b-060d-4dc9-83ea-284bef6b2aae%22%7D%5D&aoi=&page=1&sort=most-viewed&sortDirection=-1)
  This dataset gives information on what languages each country primarily speaks. It can confound the results on the similarity between the two countries' beer preferences. Our hypothesis is that same language should facilitate trade and culture. The dataset has 233 countries and has the top 3 official languages for each country. We decided to use only the official language for each country.


## Methods 

### *Step 1: Preprocessing*

##### *1. Merging*:
We were given data from two different websites - RateBeer and BeerAdvocate. To maximize our data, we merged the two datasets. We removed the intersection of users and ratings where they were matched to avoid duplicates using the matched dataset that contained users and ratings that were in both websites. We combined on the unique id’s in each field.

##### *2. Normalizing the Data*

We want to normalize the data for each aspect of ratings such as palate, taste, and aroma by subtracting each value from the mean of each year and then dividing by the standard deviation to reduce bias.

##### *3. Filtering the Data*

We plotted the data and saw very few beers with higher than 50% alcohol percentages so we removed those beers. We also removed users, and any ratings with users who had over 20,000 ratings as that was an outlier. 

##### *4. Reading in additional population datasets*

Our data consisted of users with locations and breweries with locations. The locations were either countries or states within the United States, so we combined two separate datasets on countries and US state populations to create a general population data frame. 

##### *5. Selecting Locations*
For each location, we measured the number of distinct users divided by the total population and we only wanted to look at values where that rating was high. We also excluded countries with too few users.

### *Step 2: Visualizations and Initial Analysis*

We plotted the locations we filtered out on a map, using the latitude and longitude coordinates from open street maps for each coordinate. We also plotted the brewery locations on a heatmap using a similar process. 

### *Step 3: Answering the research questions*
 
##### *Questions 1 and 2*:
We extract the most popular beer style and beer production place (brewery location) by quantity for each location by looking at the total number of ratings by year. We also put a threshold of 5 that needs to be satisfied for a location-style pair to be considered in this analysis. We will also look at the highest-rated beer style given where the number of beers for that style needs to cross a certain threshold. We look at each of the top style for each country, and then do groupings to see the distribution of different styles and how similar they are.

#### *Question 3* 
We can run Ordinary Least Squares Linear Regression on our ratings to see which aspects are the most important factors for giving each aspect a weight in comparison to taste. We were also thinking about using decision trees to predict taste based on the scores that people put in for each of the various aspects and to predict consumption. We will then test our dataset on a different subset of data to measure the accuracy.

#### *Question 4*

We will define the definition of a trend. For now, it is a style preferred in a number of countries superior to a threshold. This threshold will be optimized. We will then study trends evolutions to determine interconnexion between countries. This could be done with graph analysis, with weights combining different factors (informations on the countries).
We then want to pair the most similar locations based on 3 of the 4 categories between the number of users divided by population, distance, language, and wealth. The result is that we get locations that could be comparable on those factors. Then, we would sample half the matches with similar languages and look at their beer trends, and then sample half the matches with different matches and look at their beer trends. We can do t-tests of the data to see which factors between language, wealth, distance, and proportion of beer drinkers affect the trends the most, and if there is a correlation. 

### *Visualization*

We plan to vizualize the results on interactive heatmaps, where users can select the studied parameters. 






## Planning

1.12:
 - Interactive heatmap 
 - Trend definition and trend spreading
 - OLS linear regression and decision trees to find the most important aspects

8.12: 
 - Interconnexion between countries: graph studies
 - t-tests of the countrie's attributes that influence beer preferences

15.12: 
 - Represent the interaction/strength of links between countries on a map
 - Adding parameters to the interactive map (characteristics of the countries)
 - Combine the results and write the data story

22.12:
 - Finish the datastory
 - Finish the visualization

## Team organization

Tugba: Important aspects of beers using decision trees, create data story

Yagiz: Important aspects of beers with OLS, create data story

Hadrien: t-test for parameters that influence beer taste, representation of interaction on maps

Rishi: Interactive heatmap

Iris: Trend definition and graph analysis between countries



