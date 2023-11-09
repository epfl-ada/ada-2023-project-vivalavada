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


def location_style_stats(ratings_reviews, users, year, loc_review_threshold, loc_style_threshold):
    ratings_reviews['date'] = ratings_reviews['date'].apply(convert_unix_timestamp)
    year_filter = ratings_reviews['date'].dt.year == year
    ratings_reviews = ratings_reviews.loc[year_filter]
    ratings_reviews = pd.merge(ratings_reviews, users[['user_id', 'nbr_ratings', 'location']], on='user_id',
                               how='inner')

    location_counts = ratings_reviews['location'].value_counts()
    valid_locations = location_counts[location_counts >= loc_review_threshold].index
    ratings_reviews = ratings_reviews[ratings_reviews['location'].isin(valid_locations)]

    ratings_reviews_groupedby_loc_style = ratings_reviews.groupby(['location', 'style'])

    location_style = ratings_reviews_groupedby_loc_style.size().reset_index(name='number')
    ratings_reviews_groupedby_loc = ratings_reviews.groupby('location')
    ratings_reviews_loc = ratings_reviews_groupedby_loc.size().reset_index(name='total_loc_number')

    ratings_reviews_loc['location_mean'] = \
    ratings_reviews_groupedby_loc['rating'].mean().reset_index(name='location_mean')[
        'location_mean']
    ratings_reviews_loc['location_std'] = \
    ratings_reviews_groupedby_loc['rating'].std().reset_index(name='location_std')[
        'location_std']

    location_style = pd.merge(location_style, ratings_reviews_loc, on='location', how='inner')

    location_style['popularity_percentage'] = 100 * (location_style['number'] / location_style['total_loc_number'])
    location_style['mean_rating'] = \
    ratings_reviews_groupedby_loc_style['rating'].mean().reset_index(name='mean_rating')[
        'mean_rating']
    location_style = location_style[
        ['location', 'style', 'number', 'total_loc_number', 'popularity_percentage', 'mean_rating', 'location_mean',
         'location_std']]
    location_style['z_score'] = (location_style['mean_rating'] - location_style['location_mean']) / location_style[
        'location_std']
    location_style = location_style[location_style['number'] >= loc_style_threshold]

    return location_style
