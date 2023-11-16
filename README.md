# ada-2023-project-vivalavada
ada-2023-project-vivalavada created by GitHub Classroom

# 

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
