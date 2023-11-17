import pandas as pd
import csv
import datetime

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


def location_style_stats(ratings, users, year, loc_style_threshold):
    year_filter = ratings['year'] == year
    ratings = ratings.loc[year_filter]
    ratings = pd.merge(ratings, users[['user_id', 'nbr_ratings', 'location']], on='user_id', how='inner')

    ratings_groupedby_loc_style = ratings.groupby(['location', 'style'])

    location_style = ratings_groupedby_loc_style.size().reset_index(name='number')
    ratings_groupedby_loc = ratings.groupby('location')
    ratings_loc = ratings_groupedby_loc.size().reset_index(name='total_loc_number')

    ratings_loc['location_mean'] = ratings_groupedby_loc['rating'].mean().reset_index(name='location_mean')[
        'location_mean']
    ratings_loc['location_std'] = ratings_groupedby_loc['rating'].std().reset_index(name='location_std')[
        'location_std']

    location_style = pd.merge(location_style, ratings_loc, on='location', how='inner')

    location_style['popularity_percentage'] = 100 * (location_style['number'] / location_style['total_loc_number'])
    location_style['mean_rating'] = ratings_groupedby_loc_style['rating'].mean().reset_index(name='mean_rating')[
        'mean_rating']
    location_style = location_style[
        ['location', 'style', 'number', 'total_loc_number', 'popularity_percentage', 'mean_rating', 'location_mean',
         'location_std']]
    location_style['z_score'] = (location_style['mean_rating'] - location_style['location_mean']) / location_style[
        'location_std']
    location_style = location_style[location_style['number'] >= loc_style_threshold]

    return location_style


def location_brewery_country_stats(ratings, users, breweries, year, loc_brewery_threshold):

    year_filter = ratings['year'] == year
    ratings = ratings.loc[year_filter]

    ratings = pd.merge(ratings, users[['user_id', 'location']], on='user_id')


    breweries = breweries.rename(columns={'location': 'brewery_location'})
    ratings = pd.merge(ratings, breweries[['brewery_location', 'id']], left_on='brewery_id',
                               right_on='id')

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

    location_brewery_country = pd.merge(location_brewery_country, ratings_loc, on='location', how='inner')

    location_brewery_country['popularity_percentage'] = 100 * (location_brewery_country['number'] / location_brewery_country['total_loc_number'])

    location_brewery_country = location_brewery_country[
        ['location', 'brewery_location', 'number', 'total_loc_number', 'popularity_percentage', 'mean_rating', 'location_mean',
         'location_std']]
    location_brewery_country['z_score'] = (location_brewery_country['mean_rating'] - location_brewery_country['location_mean']) / location_brewery_country[
        'location_std']

    location_brewery_country = location_brewery_country[location_brewery_country['number'] >= loc_brewery_threshold]

    return location_brewery_country

