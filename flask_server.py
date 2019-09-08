from flask import Flask,render_template,request,jsonify
import tweepy
import requests
import datetime
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#---------------------------------------------------------------------------
# Load Keys and tokens from Textfile

keys_file = open("keys.txt")
lines = keys_file.readlines()
consumer_key = lines[0].rstrip()
consumer_secret = lines[1].rstrip()
access_token = lines[2].rstrip()
access_token_secret = lines[3].rstrip()
news_api_key = lines[4].rstrip()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#-------------------------------------------------------------------------

app = Flask(__name__)

# Home of the page
@app.route("/")
def index():
    return render_template('index.html')

# Search the wanted value either in news descriptions or tweets or both
@app.route("/search",methods=["POST"])
def search():
    analyzer = SentimentIntensityAnalyzer()
    t = []
    search_tweet = request.form.get("search_query")
    source = request.form.get("type")

    # searching in twitter tweets and evaluating it
    if source == 'twitter' or source == 'all':
        tweets = api.search(search_tweet, tweet_mode='extended')
        for tweet in tweets:
            vs = analyzer.polarity_scores(tweet.full_text)
            if vs['compound'] >= 0.05:
                sentiment = 1
            elif vs['compound'] <= -0.05:
                sentiment = -1
            else:
                sentiment = 0
            t.append([tweet.full_text, vs['pos'], vs['neu'], vs['neg'], sentiment])

    # searching in news descriptions and evaluating it but just sends back the title
    if source == 'news' or source == 'all':
        date_object = datetime.date.today()
        url = ('https://newsapi.org/v2/everything?'
               'q=' + search_tweet +
               '&language=en'
               '&from=' + str(date_object) +
               '&sortBy=popularity'
               '&apiKey=' + news_api_key)
        response = requests.get(url).json()
        if response['status'] == 'ok':
            for article in response['articles']:
                vs = analyzer.polarity_scores(article['description'])
                if vs['compound'] >= 0.05:
                    sentiment = 1
                elif vs['compound'] <= -0.05:
                    sentiment = -1
                else:
                    sentiment = 0
                t.append([article['title'], vs['pos'], vs['neu'], vs['neg'], sentiment])

    # return the data
    return jsonify({"success":True,"tweets":t})


# Run app local
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

