import json


def twitter_format(twitter):
    twitter = json.loads(twitter)
    formatted_twitter = {}
    try:
        formatted_twitter['Date'] = twitter['created_at']
        formatted_twitter['text'] = twitter['text']
        formatted_twitter['user_id'] = twitter['user']['id']
        formatted_twitter['followers_count'] = twitter['user']['followers_count']
        formatted_twitter['listed_count'] = twitter['user']['listed_count']
        formatted_twitter['statuses_count'] = twitter['user']['statuses_count']
        formatted_twitter['friends_count'] = twitter['user']['friends_count']
        formatted_twitter['favourites_count'] = twitter['user']['favourites_count']
    except:
        pass
    twitter = json.dumps(formatted_twitter)
    return twitter
