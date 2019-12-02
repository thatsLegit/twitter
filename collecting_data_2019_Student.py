import json
#import datetime
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import os
import sys
#import time


#"another" data_analytics_2019 ok
consumer_key = "•••••••••••@"
consumer_secret = "•••••••••••••••••••••@"
access_token = "•••••••••••••••••••••••••••@"
access_secret = "•••••••••••••••••••••••••••@"


os.chdir('/Users/stepanov/PycharmProjects/Twitter')

def post_status():
    oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
    # create twitter API object
    twitter = Twitter(auth=oauth)
    # post a new status
    new_status = "hi, today is 20 Nov"
    results = twitter.statuses.update(status=new_status)
    print ("updated status: %s" % new_status)

def twitter_trend():
    oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
    # create twitter API object
    twitter = Twitter(auth=oauth)
    # other localised trends can be specified by looking up Where on Earth ID-WOE IDs:
    #  http://woeid.rosselliot.co.nz/;  http://developer.yahoo.com/geo/geoplanet/
    # -----------------------------------------------------------------------
    # Get all the locations where Twitter provides trends service
    # world_trends = twitter.trends.available(_woeid=1)
    # print(world_trends)
    # Get all trending topics in San Francisco (its WOE ID is 2487956)
    print("San Francisco Trends")
    results = twitter.trends.place(_id=628886)# toulouse 628886
    #print json.dumps(results, indent=4)
    # list only names of trends.
    for location in results:
        for trend in location["trends"]:
            print(" - %s" % trend["name"])

def followers_of_user(user_name):
    oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
    # create twitter API object
    twitter = Twitter(auth=oauth)
    # Get a list friends
    results = twitter.friends.ids(screen_name=user_name, count=2000)
    #find followers
    #results = twitter.followers.ids(screen_name=user_name, count=200)
    print ("found %d followers" % (len(results["ids"])))
    # -----------------------------------------------------------------------
    for id in results['ids']:
        for user in twitter.users.lookup(user_id=id):
            print(user["screen_name"],user["location"]) # ,user["friends_count"]

def twitter_streaming(keyword,number_of_tweets):

    oauth = OAuth(access_token , access_secret, consumer_key, consumer_secret)
    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)

    # Get tweets by keyword
    iterator = twitter_stream.statuses.filter(track=keyword, language="en")

    # Print each tweet in the stream to the screen and write to a file
    tweet_count = number_of_tweets
    f_out = open('Stream_%d_%s_tweets.json' %(number_of_tweets, keyword), 'a')
    for tweet in iterator:
        tweet_count -= 1
        # Twitter Python Tool wraps the data returned by Twitter
        # as a TwitterDictResponse object.
        # We convert it back to the JSON format to print/score
        print(json.dumps(tweet))
        f_out.write(json.dumps(tweet))
        f_out.write('\n')
        # The command below will do pretty printing for JSON data, try it out
        # print json.dumps(tweet, indent=4)
        if tweet_count <= 0:
            break
    f_out.close()

def twitter_Search(keyword):

    oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
    # create twitter API object
    twitter  = Twitter(auth=oauth)
    query = twitter.search.tweets(q=keyword, lang='en', count=100)
    # time for this query to be done?
    #print("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))
    for result in query["statuses"]:
        print(result)

#######

def twitter_Search_several_tweets(keyword,number_of_tweets):  # keyword,number of tweets needed to be collected
    oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
    # create twitter API object
    twitter = Twitter(auth=oauth)
    max_id = -1
    tweet_downloaded = 0
    with open('Search_%d_%s_tweets.json' % (number_of_tweets,keyword), 'w') as f:
        while tweet_downloaded < number_of_tweets:
            try:
                if (max_id <= 0):
                    new_tweets = twitter.search.tweets(q=keyword, count=100)  # maw tweets per request 100
                else:
                    new_tweets = twitter.search.tweets(q=keyword, count=100,max_id=str(max_id - 1))
                new_tweets_status = new_tweets["statuses"]
                if not new_tweets_status:
                    print("Not found")
                    break
                for tweet in new_tweets_status:
                    f.write(json.dumps(tweet))
                    f.write('\n')
                tweet_downloaded += len(new_tweets_status)
                print("Downloaded {0} tweets".format(tweet_downloaded))
                max_id = new_tweets_status[-1]['id']
            except:
                print(" error occurs ")
                break
    print (json.dumps(new_tweets, indent=4))
    print ("There are total {0} tweets downloaded".format(tweet_downloaded))


def extracting_multiple_binary_class(file_in_tweets_json):

    f_in = open(file_in_tweets_json, "r")
    f_out = open(file_in_tweets_json +'_features.arff', "w")
    st = '@relation ' + file_in_tweets_json.split('.')[0] + '\n' + \
         '@attribute Number_of_followers numeric' + '\n' + \
         '@attribute Number_of_friend numeric' + '\n' + \
         '@attribute Total_of_tweets numeric' + '\n' + \
         '@attribute Contain_Picture {0,1}' + '\n' + \
         '@attribute Contain_hashtag {0,1}' + '\n' + \
         '@attribute @@class@@ {0,1,2,3}' + '\n' + '@data' + '\n'
    f_out.write(st)
    for line in f_in:
        tweet = json.loads(line)
        Number_of_followers = 0
        Number_of_friend = 0
        Total_of_tweets = 0
        Contain_Picture = 0
        Contain_hashtag = 0
        Retweet_class = 0
        if not tweet.get('retweeted_status'):
            Number_of_friend = tweet['user']['friends_count']
            Number_of_followers = tweet['user']['followers_count']
            Total_of_tweets = tweet['user']['statuses_count']
            if tweet['entities'].get('media'):  # check if tweet contain photo
                if tweet['entities']['media'][0]['type'] == 'photo':  # type of media ==photo
                    Contain_Picture = 1
            if tweet['entities'].get('hashtags'):  # check if tweet contain hashtag
                Contain_hashtag = 1
            Retweet_class = tweet['retweet_count']
        else:
            tweet_orginal = tweet['retweeted_status']
            Number_of_friend = tweet_orginal['user']['friends_count']
            Number_of_followers = tweet_orginal['user']['followers_count']
            Total_of_tweets = tweet_orginal['user']['statuses_count']
            if tweet_orginal['entities'].get('media'):  # check if tweet contain photo
                if tweet_orginal['entities']['media'][0]['type'] == 'photo':  # type of media ==photo
                    Contain_Picture = 1
            if tweet_orginal['entities'].get('hashtags'):  # check if tweet contain hashtag
                Contain_hashtag = 1
            Retweet_class = tweet_orginal['retweet_count']

        if Retweet_class == 0:
            Retweet_class = 0
        elif Retweet_class < 100:
            Retweet_class = 1
        elif Retweet_class < 1000:
            Retweet_class = 2
        else:
            Retweet_class = 3
        print("{0},{1},{2},{3},{4},{5}".format(Number_of_followers, Number_of_friend, Total_of_tweets, Contain_Picture, Contain_hashtag,Retweet_class))
        f_out.write("{0},{1},{2},{3},{4},{5}\n".format(Number_of_followers, Number_of_friend, Total_of_tweets, Contain_Picture, Contain_hashtag, Retweet_class))
    f_out.close()
    f_in.close()


def extracting_features_binary_class(file_in_tweets_json):

    f_in = open(file_in_tweets_json, "r")
    f_out = open(file_in_tweets_json +'_features.arff', "w")
    st = '@relation ' + file_in_tweets_json.split('.')[0] + '\n' + \
         '@attribute Number_of_followers numeric' + '\n' + \
         '@attribute Number_of_friend numeric' + '\n' + \
         '@attribute Total_of_tweets numeric' + '\n' + \
         '@attribute Contain_Picture {0,1}' + '\n' + \
         '@attribute Contain_hashtag {0,1}' + '\n' + \
         '@attribute @@class@@ {0,1}' + '\n' + '@data' + '\n'
    f_out.write(st)
    for line in f_in:
        tweet = json.loads(line)
        Number_of_followers = 0
        Number_of_friend = 0
        Total_of_tweets = 0
        Contain_Picture = 0
        Contain_hashtag = 0
        Retweet_class = 0
        if not tweet.get('retweeted_status'):
            Number_of_friend = tweet['user']['friends_count']
            Number_of_followers = tweet['user']['followers_count']
            Total_of_tweets = tweet['user']['statuses_count']
            if tweet['entities'].get('media'):  # check if tweet contain photo
                if tweet['entities']['media'][0]['type'] == 'photo':  # type of media ==photo
                    Contain_Picture = 1
            if tweet['entities'].get('hashtags'):  # check if tweet contain hashtag
                Contain_hashtag = 1
            Retweet_class = tweet['retweet_count']
        else:
            tweet_orginal = tweet['retweeted_status']
            Number_of_friend = tweet_orginal['user']['friends_count']
            Number_of_followers = tweet_orginal['user']['followers_count']
            Total_of_tweets = tweet_orginal['user']['statuses_count']
            if tweet_orginal['entities'].get('media'):  # check if tweet contain photo
                if tweet_orginal['entities']['media'][0]['type'] == 'photo':  # type of media ==photo
                    Contain_Picture = 1
            if tweet_orginal['entities'].get('hashtags'):  # check if tweet contain hashtag
                Contain_hashtag = 1
            Retweet_class = tweet_orginal['retweet_count']

        if Retweet_class > 0:
            Retweet_class = 1
        print("{0},{1},{2},{3},{4},{5}".format(Number_of_followers, Number_of_friend, Total_of_tweets, Contain_Picture, Contain_hashtag,Retweet_class))
        f_out.write("{0},{1},{2},{3},{4},{5}\n".format(Number_of_followers, Number_of_friend, Total_of_tweets, Contain_Picture, Contain_hashtag, Retweet_class))
    f_out.close()
    f_in.close()



def extracting_id(file_in_tweets_json,file_out_id_text):

    f_in = open(file_in_tweets_json, "r")
    f_out = open(file_out_id_text, "w")
    for line in f_in:
        tweet = json.loads(line)
        id = tweet['id']
        f_out.write ("%s\n" %(id))
    f_out.close()
    f_in.close()

 #-------

if __name__ == '__main__': #checks if this python script is ran directly. If yes, then the below code is executed
    #post_status()
    #followers_of_user('@Squeezie')
    #twitter_trend()
    #twitter_Search('Trump')
    #twitter_streaming('estonia',100)
    twitter_Search_several_tweets('estonia', 100)
    #extracting_features_binary_class("Search_100_estonia_tweets.json")
    #extracting_id('Search_3000_note10_tweets.json','Search_3000_note10_tweets_id1.json')
