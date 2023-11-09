import pandas as pd
import csv

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
