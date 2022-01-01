import json
import requests
import urllib
import os

IMAGES_PATH = './images'

def search_twitter(query, tweet_fields):
    BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAHOEXgEAAAAAWeA8EEpEs8ie1u6YNvjdZ6s9Ac8%3DY6gRhQ1iLBRdP0h4u24qKrsmU4HgGEDaNEUKDh6nPz4OMuYOJM'
    headers = {'Authorization': 'Bearer {}'.format(BEARER_TOKEN)}

    url = 'https://api.twitter.com/2/tweets/search/recent?query={}&{}'.format(
        query, tweet_fields
    )
    response = requests.request('GET', url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def images_for_response(json_response):
    ret = []
    for dct in json_response['data']:
        if('entities' in dct):
            entities = dct['entities']
            if('urls' in entities):
                urls = entities['urls']
                for urlDict in urls:
                    if('images' in urlDict):
                        imagesList = urlDict['images']
                        ret.append(imagesList[0]['url'])
                        # for imageDict in imagesList:
                        #     ret.append(imageDict['url'])
    return ret
def main():
    query = 'nft'
    tweet_fields = 'tweet.fields=entities'
    json_response = search_twitter(query, tweet_fields)
    image_urls = images_for_response(json_response)
    if(not os.path.exists(IMAGES_PATH)):
        os.makedirs(IMAGES_PATH)
    valid_files = [int(x.split('.')[0]) for x in os.listdir(IMAGES_PATH) if x.split('.')[0].isdigit()]
    num = 0
    if(valid_files != []): num = max(valid_files)+1
    for image_url in image_urls:
        print(image_url)
        urllib.request.urlretrieve(image_url, f'{os.path.join(IMAGES_PATH, str(num))}.jpg')
        num += 1

if (__name__ == '__main__'):
    main()