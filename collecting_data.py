import json
#import datetime
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import os
import sys
#import time


#"another" data_analytics_2019 ok
consumer_key = "KcVnz49uNPuKQFm3RQCIzFx38"
consumer_secret = "As9sHrwKarBXizcxM7D3VTRjcSs18l4YXGkHB3ExHslmZurdIi"
access_token = "726020015187726336-FstmBYu9eSTK1cZIWUJ7GoA4plHex0p"
access_secret = "5JWiCXrOG4GfvNXowu0ps39AfsDClJEHi87XLPzyAw2Gv"

os.chdir('C:/Users/pitch/PycharmProjects/Twitter')


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
        else: #Si le tweet est un RT, on va prendre le tweet original...
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


def extracting_features_binary_class_7features(file_in_tweets_json):

    f_in = open(file_in_tweets_json, "r")
    f_out = open(file_in_tweets_json +'_features.arff', "w")
    st = '@relation ' + file_in_tweets_json.split('.')[0] + '\n' + \
         '@attribute Number_of_followers numeric' + '\n' + \
         '@attribute Number_of_friend numeric' + '\n' + \
         '@attribute Total_of_tweets numeric' + '\n' + \
         '@attribute Contain_Picture {0,1}' + '\n' + \
         '@attribute Contain_hashtag {0,1}' + '\n' + \
         '@attribute langage {0,1}' + '\n' + \
         '@attribute verified_account {0,1}' + '\n' + \
         '@attribute @@class@@ {0,1}' + '\n' + '@data' + '\n'
    f_out.write(st)
    for line in f_in:
        tweet = json.loads(line)
        Number_of_followers = 0
        Number_of_friend = 0
        Total_of_tweets = 0
        Contain_Picture = 0
        Contain_hashtag = 0
        langage = 0
        verified_account = 0
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
            if tweet['user']['verified']:
                verified_account = 1
            if tweet['lang'] == "en":
                langage = 1
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
            if tweet_orginal['user']['verified']:
                verified_account = 1
            if tweet['lang'] == "en":
                langage = 1
            Retweet_class = tweet_orginal['retweet_count']

        if Retweet_class > 0:
            Retweet_class = 1
        print("{0},{1},{2},{3},{4},{5},{6},{7}".format(Number_of_followers, Number_of_friend, Total_of_tweets, Contain_Picture, Contain_hashtag, langage, verified_account, Retweet_class))
        f_out.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(Number_of_followers, Number_of_friend, Total_of_tweets, Contain_Picture, Contain_hashtag, langage, verified_account, Retweet_class))
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
    #twitter_Search_several_tweets('Estonia', 2501)
    #extracting_features_binary_class("Search_2501_estonia_tweets.json")
    #extracting_features_binary_class_7features("Search_2501_estonia_tweets.json")
    extracting_id('Search_2501_estonia_tweets.json','Search_2501_estonia_tweets.txt')