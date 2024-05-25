import csv
import re

# Function to read keywords from a file and create a dictionary
def read_keywords(keyword_file_name):
    keywords_dict = {}
    try:
        with open(keyword_file_name, 'r', encoding='utf-8') as keywords_file:
            # Loop through each line in the file
            for line in keywords_file:
                # Split the line into keyword and sentiment score
                key_value = line.strip().split("\t")
                # Check if the line has two values (keyword and sentiment score)
                if len(key_value) == 2:
                    keyword = key_value[0].lower()  # Convert keyword to lowercase
                    sentiment_score = int(key_value[1])
                    keywords_dict[keyword] = sentiment_score  # Add keyword and sentiment score to the dictionary
                else:
                    print(f"Ignore invalid line: {line}")
    except IOError:
        print(f"Could not open file {keyword_file_name}")

    return keywords_dict

# Function to clean tweet text by removing non-alphabetic characters and converting to lowercase
def clean_tweet_text(tweet_text):
    cleaned_text = ''.join(char if char.isalpha() or char.isspace() else '' for char in tweet_text)
    cleaned_text = cleaned_text.lower()
    return cleaned_text

# Function to calculate sentiment score for a tweet based on keywords
def calc_sentiment(tweet_text, keyword_dict):
    words = tweet_text.split()

    sentiment_score = 0
    for word in words:
        if word in keyword_dict:
            sentiment_score += keyword_dict[word]

    return sentiment_score

# Function to classify sentiment based on the score
def classify(score):
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        return 'neutral'

# Function to read tweets from a CSV file
def read_tweets(tweet_file_name):
    try:
        with open(tweet_file_name, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, fieldnames=['date', 'text', 'user', 'retweet', 'favorite', 'lang', 'country', 'state', 'city', 'lat', 'lon'])
            tweets = []
            for row in csv_reader:
                row['text'] = clean_tweet_text(row['text'])
                row['retweet'] = int(row['retweet'])
                row['favorite'] = int(row['favorite'])

                # Check for 'NULL' before converting to float
                row['lat'] = float(row['lat']) if row['lat'] and row['lat'].lower() != 'null' else 'NULL'
                row['lon'] = float(row['lon']) if row['lon'] and row['lon'].lower() != 'null' else 'NULl'

                tweets.append(row)
            return tweets
    except IOError:
        print(f"Could not open file {tweet_file_name}")
        return []

# Function to generate a report based on tweet data and keyword dictionary
def make_report(tweet_list, keyword_dict):
    num_tweets = len(tweet_list)
    num_favorite = 0
    num_retweet = 0
    num_positive = 0
    num_negative = 0
    num_neutral = 0
    total_sentiment_score = 0
    total_favorite_sentiment_score = 0
    total_retweet_sentiment_score = 0
    country_sentiment_scores = {}

    for tweet in tweet_list:
        text = tweet['text']
        favorite = tweet['favorite']
        retweet = tweet['retweet']

        # Calculate sentiment score for the tweet
        sentiment_score = calc_sentiment(text, keyword_dict)
        total_sentiment_score += sentiment_score

        # Classify sentiment of the tweet
        sentiment_class = classify(sentiment_score)
        if sentiment_class == 'positive':
            num_positive += 1
        elif sentiment_class == 'negative':
            num_negative += 1
        else:
            num_neutral += 1

        # Count favorited and retweeted tweets
        if int(favorite) > 0:
            num_favorite += 1
            total_favorite_sentiment_score += sentiment_score

        if int(retweet) > 0:
            num_retweet += 1
            total_retweet_sentiment_score += sentiment_score

        # Get the country of the tweet
        country = tweet.get('country', 'N/A')
        # Check if the country is not 'N/A' and not 'NULL'
        if country != 'N/A' and country.lower() != 'null':
            if country not in country_sentiment_scores:
                country_sentiment_scores[country] = []
            country_sentiment_scores[country].append(sentiment_score)

    # Calculate average sentiment scores
    avg_sentiment = round(total_sentiment_score / num_tweets, 2) if num_tweets > 0 else 'NAN'
    avg_favorite_sentiment = round(total_favorite_sentiment_score / num_favorite, 2) if num_favorite > 0 else 'NAN'
    avg_retweet_sentiment = round(total_retweet_sentiment_score / num_retweet, 2) if num_retweet > 0 else 'NAN'

    avg_country_sentiment_scores = {}
    # Calculate average sentiment scores for each country
    for country, scores in country_sentiment_scores.items():
        avg_country_sentiment_scores[country] = round(sum(scores) / len(scores), 2)

    # Exclude 'N/A' and 'NULL' from top five countries
    top_five_countries = sorted(
        (country for country in avg_country_sentiment_scores if country.lower() not in {'n/a', 'null'}),
        key=avg_country_sentiment_scores.get,
        reverse=True
    )[:5]

    top_five_str = ', '.join(top_five_countries)

    # Create a report dictionary
    report = {
        'avg_favorite': avg_favorite_sentiment,
        'avg_retweet': avg_retweet_sentiment,
        'avg_sentiment': avg_sentiment,
        'num_favorite': num_favorite,
        'num_negative': num_negative,
        'num_neutral': num_neutral,
        'num_positive': num_positive,
        'num_retweet': num_retweet,
        'num_tweets': num_tweets,
        'top_five': top_five_str
    }

    return report

# Function to write the report to a file
def write_report(report, output_file):
    try:
        with open(output_file, 'w') as report_file:
            # Write various statistics to the report file
            report_file.write(f"Average sentiment of all tweets: {report['avg_sentiment']}\n")
            report_file.write(f"Total number of tweets: {report['num_tweets']}\n")
            report_file.write(f"Number of positive tweets: {report['num_positive']}\n")
            report_file.write(f"Number of negative tweets: {report['num_negative']}\n")
            report_file.write(f"Number of neutral tweets: {report['num_neutral']}\n")
            report_file.write(f"Number of favorited tweets: {report['num_favorite']}\n")
            report_file.write(f"Average sentiment of favorited tweets: {report['avg_favorite']}\n")
            report_file.write(f"Number of retweeted tweets: {report['num_retweet']}\n")
            report_file.write(f"Average sentiment of retweeted tweets: {report['avg_retweet']}\n")
            report_file.write(f"Top five countries by average sentiment: {report['top_five']}\n")
        print(f"Wrote report to {output_file}")
    except IOError:
        print(f"Could not open file {output_file}")






