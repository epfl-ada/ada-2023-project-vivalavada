# ada-2023-project-vivalavada
ada-2023-project-vivalavada created by GitHub Classroom

## How do beer trends evolve with time? 

## Abstract 

We propose in this study to analyze how different locale's beer preferences change with regards to the distance between different regions over time. As technology and transportation has increased, for example, we want to see if Canadians may drink more beer from the United States over time because of their relative proximity as opposed to drinking more beer from France since France is further away. Our dataset gives the style for each rating that people drink, and we can also measure how much people from a specific region are drinking each style. We shall investigate many different metrics to check the popularity of different styles of beer over time, such as the styles that are most consumed, the styles with the highest ratings, and the number of breweries that primarily produce a certain style. Our motivation is to see whether countries that are close together geographically have become more interconnected over time through the lens of beer. 

## Research Questions

1. What style of beers have the highest rating, and alternatively, which ones are consumed the most? Among the different categories that are given such as palate, taste, and creativity, what plays the biggest role in determining the style rating and the consumption? Does it differ from region to region? 

2. How does the popularity and style rating for each type of beer change over the years for a specific location? For each region of interest, we want to look at the distribution of beers they are consuming and the beers they are giving the highest ratings to, and see if that is spreading out more with time. 

3. Do some countries mirror the same habits of other countries in terms of the metrics we defined above, and if so, how closely are these countries linked? We especially want to investigate if there is a correlation between the types of beer that they are consuming and the distance between two regions. For example, we'd expect that over time due to increased globalization, Swiss people would get access to more French beer because the two countries are so close in a geographic sense, but it would be more surprising if Americans suddenly started consuming Australian beer. 

4. Can we notice some general trends regarding the distributions of beer that countries consume over time, and how does it shift? Is the world's beer preference in terms of style rating and consumption becoming more homogenous, or are beer preferences still generally confined to a specific region

## Additional Datasets 

1. [Country Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset): We wanted to strictly analyze countries that have a high ratio of users in comparison to the population so that we know we are getting a large enough sample. Beyond that, population gives us a further parameter to analyze the trends of each country, as the population could be another confounding variable that explains why certain countries start giving higher ratings and consuming beers from other countries. We were able to merge our existing datasets of users, ratings, and breweries with the population dataset based on the attribute of location. A lot of users were from countries outside the US, while others were from states inside the US. We used the latest population year that they gave us (*which was 2022*)

2. [Us State Population Dataset](https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html): Many users are from distinct states in the United States, but we still want to separate regions so we had to get the population for each state of the United States as well. Our motivations for using this dataset are the same as using the Country Population dataset, where we wanted to decide on a list of locations where the number of users from each country was a large enough proportion of their population. After doing preprocessing on the locations field of the users' dataset, we were able to determine whether a user was from the United States, and then we could uniquely identify the state. We then merged with the US population dataset on the common fields of location. Multiple years were given, but we chose 2022 to be consistent with the country years as well.

3. [Languages Dataset](https://resourcewatch.org/data/explore/soc_071_world_languages?section=Discover&selectedCollection=&zoom=3&lat=0&lng=0&pitch=0&bearing=0&basemap=dark&labels=light&layers=%5B%7B%22dataset%22%3A%2220662342-dcdd-4a42-9f58-bcc80217de71%22%2C%22opacity%22%3A1%2C%22layer%22%3A%22f2d76e6b-060d-4dc9-83ea-284bef6b2aae%22%7D%5D&aoi=&page=1&sort=most-viewed&sortDirection=-1)
   We also wanted information on what languages each country primarily spoke because that could confound the results on the similarity between the two countries' beer preferences. For example, if two countries were right next to each other, but they had different languages, perhaps they would be a bit more unlikely to facilitate trade and culture. The dataset has 233 countries and has the top 3 official languages for each country. We decided to use only the official language for each country to simplify everything, and we could merge that with users and breweries again. 


## Methods 

### Step 1: Preprocessing 

1. Filtering: In this step, we removed the outliers. For now, NaN were not remove, since all rows contain relevant information. Outliers were found, with beers having an alcohol content reaching 70° wich is very unprobable([Beers Wikipedia](https://en.wikipedia.org/wiki/Beer#:~:text=Beer%20ranges%20from%20less%20than,by%20the%20freeze%2Ddistilling%20process)). 34 duplicates in ratings were found (same user rates the same beer, the same year) and only one was kept. The data was also filtered to only keep locations with sufficient number of ratings. 
 
2. Merging: We merged the data from the two websites in order to double the number of data. However, this merging needed to take into account multiple factors. First, some users and ratings were duplicated between the two websites. The duplicated rating were all removed. The deplicated users were merged together, by keeping the user-id corresponding to RateBeer. Secondly, the style’s name weren’t the same between the websites. Using the beers.csv of the matched_dataset, a dictionary was created, associating the beer style of BeerAdvocate to the most frequent RateBeer style associated.

3. Normalization of the ratings: Since overall mean in rating tends to increase with time, and that it is disparate accross websites, we computed z-score for each rating and sub-rating. The z-score is then taken using the mean and standard deviation for each website and for each year.

### Step 2: Answering research questions 

1. Analyze the most popular styles:  extract the ratings of each style, and the number of ratings per style. In order to study the influence of the different aspects of a beer, a regression will be made, and we will compute the correlation between each sub-rating and the overall rating. These studies will be made for the different locations. 

2. Analyze of the variations in time of the previous metrics (for each year, or for each period during one year). These first analysis will allow us to define a trend: for now, the definition would be a style preferred in a number of countries superior to a threshold. This threshold will be optimized according to the results of preferred styles obtained. Once a final definition of trend will be adopted, we will be able to study how they evolve, for example their duration.

3. Once those trends are analyzed, we will be able to compare the countries and study their inter-connexion. We will create a graph of the countries, with the weights influenced by the number of shared trends, but also other aspects as the physical distance or the cultural differences (such as language). Correlation between the difference in trends and different countries informations could also be computed. 

4. Finally, we will be able to analyze the patterns of the trends, for example by comparing the number of trends with time, or their different aspects mentioned before. Statistical analysis will be led, to quantify if there is a relationship between the countries. 

### Step 3: Visualization

The goal is to create an interactive map. We could set parameters such as timescale, styles and countries to study. Then, the map could show the evolution of the trends with time. 

## Planning

## Team organization


