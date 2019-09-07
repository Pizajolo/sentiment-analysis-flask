from flask import Flask,render_template,request,jsonify
import tweepy
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#---------------------------------------------------------------------------

consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#-------------------------------------------------------------------------

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search",methods=["POST"])
def search():
    search_tweet = request.form.get("search_query")
    t = []
    tweets = api.search(search_tweet, tweet_mode='extended')
    analyzer = SentimentIntensityAnalyzer()
    for tweet in tweets:
        vs = analyzer.polarity_scores(tweet.full_text)
        if vs['compound'] > 0.5:
            sentiment = 1
        elif vs['compound'] < -0.5:
            sentiment = -1
        else:
            sentiment = 0
        t.append([tweet.full_text, vs, sentiment])
    return jsonify({"success":True,"tweets":t})


# Run app local
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

