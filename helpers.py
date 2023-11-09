import pandas as pd
import csv

def txt_to_csv():
    # Script to convert the ratings and reviews txt files to csv files
    FILE = 'data/RateBeer/ratings-reviews.txt'

    # Read the text file and split it into reviews
    with open(FILE, 'r', encoding='utf-8') as file:
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
    with open(FILE.replace('txt', 'csv'), 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reviews_data[0].keys())
        writer.writeheader()
        writer.writerows(reviews_data)
