import pandas as pd
import csv
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap
from IPython.display import display
from geopy.distance import geodesic
import math
from statsmodels.stats import diagnostic
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf


def txt_to_csv(file_path):
    # Script to convert the ratings and reviews txt files to csv files
    # Gets the file path as input

    # Read the text file and split it into reviews
    with open(file_path, 'r', encoding='utf-8') as file:
        reviews_text = file.read().strip().split('\n\n')

    # Process each review and extract the data
    reviews_data = []
    for review_text in reviews_text:
        review_data = {}
        for line in review_text.split('\n'):
            key, value = line.split(': ', 1)
            review_data[key] = value
        reviews_data.append(review_data)


    # Write the data to a CSV file
    with open(file_path.replace('txt', 'csv'), 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reviews_data[0].keys())
        writer.writeheader()
        writer.writerows(reviews_data)


def convert_unix_timestamp(unix_timestamp):
    timestamp = datetime.datetime.utcfromtimestamp(unix_timestamp)
    return timestamp


def location_style_stats(ratings, users, year, loc_style_threshold, rating_flag, global_flag = False):
    year_filter = ratings['year'] == year
    ratings = ratings.loc[year_filter]
    ratings = pd.merge(ratings, users[['user_id', 'nbr_ratings', 'location']], on='user_id', how='inner')

    if global_flag:
        ratings['location'] = ratings['location'].apply(lambda x: 'United States' if 'United States' in x else x)

    ratings_groupedby_loc_style = ratings.groupby(['location', 'style'])

    location_style = ratings_groupedby_loc_style.size().reset_index(name='number')
    ratings_groupedby_loc = ratings.groupby('location')
    ratings_loc = ratings_groupedby_loc.size().reset_index(name='total_loc_number')

    ratings_loc['location_mean'] = ratings_groupedby_loc['rating'].mean().reset_index(name='location_mean')[
        'location_mean']
    ratings_loc['location_std'] = ratings_groupedby_loc['rating'].std().reset_index(name='location_std')[
        'location_std']
    ratings_loc['location_std'] = ratings_loc['location_std'].fillna(1)

    location_style = pd.merge(location_style, ratings_loc, on='location', how='inner')

    location_style['popularity_percentage'] = 100 * (location_style['number'] / location_style['total_loc_number'])
    location_style['mean_rating'] = ratings_groupedby_loc_style['rating'].mean().reset_index(name='mean_rating')[
        'mean_rating']

    location_style_groupedby_style = location_style.groupby('style')
    style_means = location_style_groupedby_style['popularity_percentage'].mean().to_dict()
    style_stds = location_style_groupedby_style['popularity_percentage'].std().to_dict()

    location_style['popularity_z_score'] = location_style.apply(lambda x:
                                        (x['popularity_percentage'] - style_means[x['style']]) / style_stds[x['style']], axis = 1)


    location_style['z_score'] = (location_style['mean_rating'] - location_style['location_mean']) / location_style[
        'location_std']

    location_style = location_style[
        ['location', 'style', 'number', 'total_loc_number', 'popularity_percentage', 'popularity_z_score',
        'mean_rating', 'location_mean','location_std', 'z_score']]

    if rating_flag == True:
        loc_list = location_style['location'].unique()
        filtered_loc_list = location_style[location_style['number'] >= loc_style_threshold][
            'location'].unique()
        locs_filtered_out = set(loc_list) - set(filtered_loc_list)
        location_style_filtered_out = location_style[
            location_style['location'].isin(locs_filtered_out)]
        half_thr = location_style_filtered_out[
            location_style_filtered_out['number'] >= int(loc_style_threshold / 2)]
        full_thr = location_style[location_style['number'] >= loc_style_threshold]
        location_style = pd.concat([full_thr, half_thr])

    else:
        global_threshold = 0.0
        location_style = location_style[location_style['popularity_z_score'] > global_threshold]

    return location_style


def location_brewery_country_stats(ratings, users, breweries, year, loc_brewery_threshold, rating_flag, global_flag = False):

    year_filter = ratings['year'] == year
    ratings = ratings.loc[year_filter]

    ratings = pd.merge(ratings, users[['user_id', 'location']], on='user_id')


    breweries = breweries.rename(columns={'location': 'brewery_location'})
    ratings = pd.merge(ratings, breweries[['brewery_location', 'id']], left_on='brewery_id',
                               right_on='id')

    if global_flag:
        ratings['location'] = ratings['location'].apply(lambda x: 'United States' if 'United States' in x else x)

    ratings_gb_loc_brew_loc = ratings.groupby(['location', 'brewery_location'])
    location_brewery_country = ratings_gb_loc_brew_loc.size().reset_index(name='number')
    location_brewery_country['mean_rating'] = ratings_gb_loc_brew_loc['rating'].mean().reset_index(name='mean_rating')[
            'mean_rating']

    ratings_gb_loc = ratings.groupby('location')
    ratings_loc = ratings_gb_loc.size().reset_index(name='total_loc_number')
    ratings_loc['location_mean'] = ratings_gb_loc['rating'].mean().reset_index(name='location_mean')[
        'location_mean']
    ratings_loc['location_std'] = ratings_gb_loc['rating'].std().reset_index(name='location_std')[
        'location_std']
    ratings_loc['location_std'] = ratings_loc['location_std'].fillna(1)

    location_brewery_country = pd.merge(location_brewery_country, ratings_loc, on='location', how='inner')

    location_brewery_country['popularity_percentage'] = 100 * (location_brewery_country['number'] / location_brewery_country['total_loc_number'])
    location_brewery_country_groupedby_brew_location = location_brewery_country.groupby('brewery_location')
    brew_loc_means = location_brewery_country_groupedby_brew_location['popularity_percentage'].mean().to_dict()
    brew_loc_stds = location_brewery_country_groupedby_brew_location['popularity_percentage'].std().to_dict()

    location_brewery_country['popularity_z_score'] = location_brewery_country.apply(lambda x:
                                                                (x['popularity_percentage'] - brew_loc_means[x['brewery_location']]) /
                                                                brew_loc_stds[x['brewery_location']], axis=1)

    location_brewery_country['z_score'] = (location_brewery_country['mean_rating'] - location_brewery_country[
        'location_mean']) / location_brewery_country['location_std']


    location_brewery_country = location_brewery_country[
        ['location', 'brewery_location', 'number', 'total_loc_number', 'popularity_percentage', 'popularity_z_score',
        'mean_rating', 'location_mean','location_std', 'z_score']]

    if rating_flag == True:
        loc_list = location_brewery_country['location'].unique()
        filtered_loc_list = location_brewery_country[location_brewery_country['number'] >= loc_brewery_threshold]['location'].unique()
        locs_filtered_out = set(loc_list) - set(filtered_loc_list)
        location_brewery_country_filtered_out = location_brewery_country[location_brewery_country['location'].isin(locs_filtered_out)]
        half_thr = location_brewery_country_filtered_out[location_brewery_country_filtered_out['number'] >= int(loc_brewery_threshold/2)]
        full_thr = location_brewery_country[location_brewery_country['number'] >= loc_brewery_threshold]
        location_brewery_country = pd.concat([full_thr, half_thr])

    else:
        global_threshold = 0.0
        location_brewery_country = location_brewery_country[location_brewery_country['popularity_z_score'] > global_threshold]

    return location_brewery_country



# Gets latitude and longitude of each location
def geocode_location(location_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Similarity metric between two lists through set intersection
def jaccard(list1, list2): 
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(set(list1)) + len(set(list2))) - intersection
    return float(intersection) / union

def compute_similarity_countries(df_ranking, ll_dict, jaccard_flag = True, ):
    from geopy.distance import geodesic
    all_years_list = sorted(df_ranking.columns.unique())
    countries = df_ranking.index.tolist()
    pairwise_similarity = pd.DataFrame()
    for year in all_years_list:
        similarities = []
        df_ranking_year = df_ranking[str(year)]
        for i in range(len(df_ranking_year)):
            for j in range(i+1, len(df_ranking_year)):
                if (jaccard_flag): 
                    similarity = jaccard(df_ranking_year.iloc[i],df_ranking_year.iloc[j])
                else: 
                    distance = geodesic(ll_dict[df_ranking_year.iloc[i]], ll_dict[df_ranking_year.iloc[j]]).kilometers
                    similarity = 1/(distance+1000)
                
                similarities.append((countries[i], countries[j], similarity))

        df_similarities = pd.DataFrame(similarities, columns=['Country 1', 'Country 2', 'Similarity - ' + str(year)])
        pairwise_similarity=pd.concat([pairwise_similarity, df_similarities], axis=1)
    
    pairwise_similarity = pairwise_similarity.T.drop_duplicates().T
    return pairwise_similarity


def plot_similarity_evolution(df_similarity):
    #title_dictionary = {str(style_similarity_ratings) : 'Similarity of Style Ratings Each Year', str(style_similarity_popularity) : 'Similarity of Consumption of Beer Styles Each Year',
     #str(mean_global_similarity_ratings) : 'Global beer consumption styles each year', str(brewery_similarity_popularity) : 'Top brewery similarity based on Consumption',
      #str(brewery_similarity_ratings) : 'Top brewery similarity based on Ratings', str(brewery_similarity_to_global_pop) : 'Brewery consumption similarity compared to global popularity', str(brewery_similarity_to_global_ratings) : 'brewery rating similarity compared to global popularity'}
    all_columns = df_similarity.columns.tolist()
    rename_columns = {}
    similarity_columns = []
    for column in all_columns:
        if column.startswith('Similarity'):
            rename_columns[column] = column[len('Similarity - '): ]
            similarity_columns.append(rename_columns[column])
        else:
            rename_columns[column] = column
    df_similarity_copy = df_similarity.copy()
    df_similarity_copy.columns = rename_columns.values()
    plt.figure(figsize=(8,6))
    #plt.title(title_dictionary[str(df_similarity)])
    plt.xlabel('similarity')
    plt.ylabel('year')
    sns.pointplot(data=df_similarity_copy[similarity_columns])
    plt.show()

import math

# Function taken from GeeksForGeeks
def haversine(lat1, lon1, lat2, lon2): 
    dLat = (lat2 - lat1) * math.pi / 180.0 # Get distance between each of the lats and longs and convert to radians
    dLon = (lon2 - lon1) * math.pi / 180.0
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
    # apply formula
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2));
    RADIUS = 6371 # Approximate radius of the earth in kilometers
    c = 2 * math.asin(math.sqrt(a))
    return RADIUS * c


def get_lat_long(percentage_users_by_location):
    from geopy.geocoders import Nominatim
    latitudes_longitudes = {}
    geolocator = Nominatim(user_agent="my_geocoder")
    for location in percentage_users_by_location['location'].tolist():
        geocode_location = geolocator.geocode(location)
        if geocode_location:
            latitudes_longitudes[location] = (geocode_location.latitude, geocode_location.longitude)
    return latitudes_longitudes

def get_location_df(latitudes_longitudes):
    location_distances_dict = {}
    for first_location in latitudes_longitudes:
        location_distances_dict[first_location] = {}
        for second_location in latitudes_longitudes:
            if first_location == second_location:
                location_distances_dict[first_location][second_location] = 0
            if first_location != second_location:
                location_distances_dict[first_location][second_location] = haversine(latitudes_longitudes[first_location][0], latitudes_longitudes[first_location][1], latitudes_longitudes[second_location][0], latitudes_longitudes[second_location][1])
    return location_distances_dict, pd.DataFrame(location_distances_dict)

def k_closest_and_farthest_locations(k, all_differences_dict): # returns the k closest locations to the current location and the k furthest locations to the current location based on differences between each location
    k_closest_locs = {}
    k_farthest_locs = {}
    for location in all_differences_dict:
        sorted_locations_by_distance = sorted(all_differences_dict[location].items(), key=lambda x:x[1])
        k_closest_locs[location] = sorted_locations_by_distance[1: k + 1]
        k_farthest_locs[location] = sorted_locations_by_distance[len(all_differences_dict) - k : len(all_differences_dict) ]
    return k_closest_locs, k_farthest_locs


def get_group_similarities(ratings, df_ranking, k_closest_locs, k_farthest_locs, ll_dict, jaccard_flag = True): 
    all_years_list = sorted(ratings['year'].unique())
    countries = df_ranking.index.tolist()
    closest_sim_tot = pd.DataFrame()
    farthest_sim_tot = pd.DataFrame()
    for year in all_years_list:
        df_ranking_year = df_ranking[str(year)]
        closest_sim = []
        farthest_sim = []
        for i in range(len(df_ranking_year)):
            k_closest = k_closest_locs[countries[i]]
            k_farthest = k_farthest_locs[countries[i]]
            if (jaccard_flag):
                for loc in (k_closest) : 
                    distance = jaccard(df_ranking_year.iloc[i],df_ranking_year[loc[0]])
                    closest_sim.append(distance)
                
                for loc in (k_farthest) : 
                    distance = jaccard(df_ranking_year.iloc[i],df_ranking_year[loc[0]])
                    farthest_sim.append(distance)
            else: 
                for loc in (k_closest) : 
                    distance = geodesic(ll_dict[df_ranking_year.iloc[i]], ll_dict[df_ranking_year[loc[0]]]).kilometers
                    similarity = 1/(distance+1000)
                    
                    closest_sim.append(similarity)
                
                for loc in (k_farthest) : 
                    distance = geodesic(ll_dict[df_ranking_year.iloc[i]], ll_dict[df_ranking_year[loc[0]]]).kilometers
                    similarity = 1/(distance+1000)
                    farthest_sim.append(similarity)

        df_closer= pd.DataFrame(closest_sim, columns=['Similarity Close - ' + str(year)])
        df_farthest= pd.DataFrame(farthest_sim, columns=['Similarity Far - ' + str(year)])
        
        closest_sim_tot=pd.concat([closest_sim_tot, df_closer], axis=1)
        farthest_sim_tot = pd.concat([farthest_sim_tot, df_farthest], axis=1)
    return closest_sim_tot, farthest_sim_tot

def plot_graphs(similarity_columns, closest_ratings, farthest_ratings, global_ratings, closest_pop, farthest_pop, global_pop, brewery_or_style = 'style', wealth_flag = 'wealth'):
    fig, axs = plt.subplots(1, 2, figsize=(16, 6)) # Make the graphs

    axs[0].scatter(similarity_columns, closest_ratings.mean(), label='Closest locations in terms of  ' + str(wealth_flag) + ' - ' + str(brewery_or_style) + ' ratings mean')
    axs[0].plot(similarity_columns, closest_ratings.mean(), linestyle='-', marker='', color='blue')

    axs[0].scatter(similarity_columns, farthest_ratings.mean(), label='Farthest locations in terms of  ' + str(wealth_flag) + ' - ' + str(brewery_or_style) + ' popularity mean')
    axs[0].plot(similarity_columns, farthest_ratings.mean(), linestyle='-', marker='', color='orange')

    axs[0].scatter(similarity_columns, global_ratings.iloc[:, 2:].mean(), label='Global ' + str(brewery_or_style) +   ' similarity Ratings mean') # Plotting global style ratings mean using style similarity ratings calculated for global
    axs[0].plot(similarity_columns, global_ratings.iloc[:, 2:].mean(), linestyle='-', marker='', color='green')


    axs[0].set_title( str(brewery_or_style) + ' Similarity Based on Ratings')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Similarity')
    axs[0].legend()


    axs[1].scatter(similarity_columns, closest_pop.mean(), label='Closest locations in terms of  ' + str(wealth_flag) + ' - ' + str(brewery_or_style) + ' popularity mean')
    axs[1].plot(similarity_columns, closest_pop.mean(), linestyle='-', marker='', color='blue')

    axs[1].scatter(similarity_columns, farthest_pop.mean(), label='Farthest locations in terms of  ' + str(wealth_flag) + ' - ' + str(brewery_or_style) + ' popularity mean')
    axs[1].plot(similarity_columns, farthest_pop.mean(), linestyle='-', marker='', color='orange')

    axs[1].scatter(similarity_columns, global_pop.iloc[:, 2:].mean(), label='Global ' + str(brewery_or_style) + ' popularity mean')
    axs[1].plot(similarity_columns, global_pop.iloc[:, 2:].mean(), linestyle='-', marker='', color='green')


    axs[1].set_title( str(brewery_or_style) + ' Similarity Based on Popularity')
    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('Similarity')
    axs[1].legend()


    plt.show()


def t_test_dataframe(similarity_columns, closest_ratings, farthest_ratings, global_ratings, closest_pop, farthest_pop, global_pop):
    from scipy import stats
    df_all_years = {'year' : [], 'closest vs furthest p value for rating': [], 'closest vs furthest p value based on consumption': []}
    for i in range(2006, 2018):
        string_year = str(i)
        t_statistic, p_ratings_value = stats.ttest_ind(closest_ratings[string_year],farthest_ratings[string_year])
        df_all_years['year'].append(string_year)
        df_all_years['closest vs furthest p value for rating'].append(p_ratings_value)
        t_statistic, p_pop_value = stats.ttest_ind(closest_pop[string_year],farthest_pop[string_year])
        df_all_years['closest vs furthest p value based on consumption'].append(p_pop_value)
    return pd.DataFrame(df_all_years)


def prepare_data_plot(df, inverted_location_dict, year): 
    df_jaccard = df[['Country 1', 'Country 2', 'Similarity - ' + str(year)]]
    df_jaccard.rename(columns={'Country 1': 'source', 'Country 2': 'target', 'Similarity - '+str(year): 'weight'}, inplace=True)
    df_jaccard = df_jaccard.replace(inverted_location_dict)
    df_jaccard = df_jaccard[df_jaccard['weight'] != 0]
    str_to_int = dict(zip(c['nodes'], c.index))
    df_jaccard['source'] = df_jaccard['source'].replace(str_to_int)
    df_jaccard['target'] = df_jaccard['target'].replace(str_to_int)

    return df_jaccard[['source', 'target', 'weight']]


