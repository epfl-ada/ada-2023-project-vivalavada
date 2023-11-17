# ada-2023-project-vivalavada
ada-2023-project-vivalavada created by GitHub Classroom

## How do beer trends evolve with time? 


## Abstract 

We propose in this study to analyze how different regions' beer preferences change with regard to the distance between neighboring places over time. As technology and transportation has increased, for example, we want to see if Canadians may drink more beer from the United States over time because of their relative proximity as opposed to drinking more beer from France since France is further away. We shall investigate many different metrics to check the popularity of different styles of beer over time, such as the styles that are most consumed, the styles with the highest ratings, and the number of breweries that primarily produce a certain style. Our motivation is to see whether countries that are close together geographically have become more interconnected over time through the lens of beer, and what factors make certain styles popular. 

## Research Questions

1.  The first question we want to ask is what beers are the most popular and what factors of a beer determine popularity. To do this, we have the specific subquestions: What style of beers have the highest rating, and alternatively, which ones are consumed the most? Among the different categories that are given such as palate, taste, and creativity, what plays the biggest role in determining the style rating and the consumption? 

2. Is the world's beer preference in terms of style rating and consumption becoming more similar over time, or are beer preferences still generally confined to a specific region

2. How does the popularity and style rating for each type of beer change over the years for a specific location? For each region of interest, we want to look at the distribution of beers they are consuming and the beers they are giving the highest ratings to, and see if that is spreading out more with time. 

3. Do some countries share the same habits of other countries in terms of the metrics we defined above, and if so, how closely are these countries linked? We especially want to investigate if there is a correlation between the types of beer that they are consuming and the distance between the two regions. 



## Additional Datasets 

1. [Country Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset): We wanted to strictly analyze countries that have a high ratio of users in comparison to the population so that we know we are getting a large enough sample. Beyond that, population gives us a further parameter to analyze the trends of each country, as the population could be another confounding variable that explains why certain countries start giving higher ratings and consuming beers from other countries. We were able to merge our existing datasets of users, ratings, and breweries with the population dataset based on the attribute of location. A lot of users were from countries outside the US, while others were from states inside the US. We used the latest population year that they gave us (*which was 2022*)

2. [Us State Population Dataset](https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html): Many users are from distinct states in the United States, but we still want to separate regions so we had to get the population for each state of the United States as well. Our motivations for using this dataset are the same as using the Country Population dataset, where we wanted to decide on a list of locations where the number of users from each country was a large enough proportion of their population. After doing preprocessing on the locations field of the users' dataset, we were able to determine whether a user was from the United States, and then we could uniquely identify the state. We then merged with the US population dataset on the common fields of location. Multiple years were given, but we chose 2022 to be consistent with the country years as well.

3. [Languages Dataset](https://resourcewatch.org/data/explore/soc_071_world_languages?section=Discover&selectedCollection=&zoom=3&lat=0&lng=0&pitch=0&bearing=0&basemap=dark&labels=light&layers=%5B%7B%22dataset%22%3A%2220662342-dcdd-4a42-9f58-bcc80217de71%22%2C%22opacity%22%3A1%2C%22layer%22%3A%22f2d76e6b-060d-4dc9-83ea-284bef6b2aae%22%7D%5D&aoi=&page=1&sort=most-viewed&sortDirection=-1)
   We also wanted information on what languages each country primarily spoke because that could confound the results on the similarity between the two countries' beer preferences. For example, if two countries were right next to each other, but they had different languages, perhaps they would be a bit more unlikely to facilitate trade and culture. The dataset has 233 countries and has the top 3 official languages for each country. We decided to use only the official language for each country to simplify everything, and we could merge that with users and breweries again. 


## Methods 

### *Step 1: Preprocessing*

##### *1. Merging*:
We were given data from two different websites - RateBeer and BeerAdvocate. To maximize our data, we felt that merging the two datasets would be useful. We removed the intersection of users and ratings where they were matched to avoid duplicates using the matched dataset that contained users and ratings that were in both websites. We combined on the unique id’s in each field.

##### *2. Normalizing the Data*

We want to normalize the data for each aspect of ratings such as palate, taste and aroma by subtracting each value from the mean and then dividing by the standard deviation 

##### *3. Filtering the Data*

We plotted the data and saw very few beers with higher than 50% alcohol percentages so we removed those beers. We also removed users, and any ratings with users who had over 20,000 ratings as that was an outlier. 

##### *4. Reading in additional population datasets*

Our data consisted of users with locations and breweries with locations. The locations were either countries or states within the United States, so we combined two separate datasets on countries and US state populations to create a general population data frame. 

5. Selecting Locations
For each location, we measured the number of distinct users divided by the total population and we only wanted to look at values where that rating was high. We also excluded countries with too few users.

### *Step 2: Visualizations and Initial Analysis*

We plotted the locations we filtered out on a map, using the latitude and longitude coordinates from open street maps for each coordinate. We also plotted the brewery locations on a heatmap using a similar process. 

### *Step 3: Looking at style preferences over time*
 
We extract the highest-rated beer style for each location by looking at the average rating by year. We also put a threshold of 5 that needs to be satisfied for a location-style pair to be considered in this analysis.

## Planning

## Team organization

## How do beer trends evolve with time? 

