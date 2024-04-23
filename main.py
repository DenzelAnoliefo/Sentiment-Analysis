from sentiment_analysis import read_keywords, read_tweets, make_report, write_report

def main():
        # Get input filenames from the user
        keyword_filename = input("Input keyword filename (.tsv file): ")
        if not keyword_filename.endswith('.tsv'):
            raise Exception("Must have tsv file extension!")

        tweet_filename = input("Input tweet filename (.csv file): ")
        if not tweet_filename.endswith('.csv'):
            raise Exception("Must have csv file extension!")

        report_filename = input("Input filename to output report in (.txt file): ")
        if not report_filename.endswith('.txt'):
            raise Exception("Must have txt file extension!")


        keywords = read_keywords(keyword_filename)
        tweets = read_tweets(tweet_filename)
        report = make_report(tweets, keywords)
        write_report(report, report_filename)

main()



