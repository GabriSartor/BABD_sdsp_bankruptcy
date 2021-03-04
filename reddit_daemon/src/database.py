import requests
from ratelimit import limits, sleep_and_retry

MINUTE = 60

@sleep_and_retry
@limits(calls=20, period=MINUTE)
def get_submissions(url, field_list = "", subreddit_list = "", before = "", after = ""):
    payload = {'fields' : field_list, 'subreddit' : subreddit_list, 
                'after' : after, 'before' : before, 'size' : 100}
    response = requests.get(url, payload)
    
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response

@sleep_and_retry
@limits(calls=20, period=MINUTE)
def get_comments_id(url, id):
    response = requests.get(url+'/{}'.format(id))
    
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response

@sleep_and_retry
@limits(calls=20, period=MINUTE) 
def get_comments(url, field_list = "", id_list = ""):
    payload = {'fields' : field_list, 'ids' : id_list, 'size' : len(id_list)}
    response = requests.get(url, payload)
    
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response