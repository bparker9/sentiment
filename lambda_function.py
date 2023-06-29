import json
from sys import getsizeof
import re
import math
import collections, functools, operator
from datetime import datetime
import boto3
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

client = boto3.client('comprehend')
s3_client = boto3.client('s3', region_name='us-east-1')
s3 = boto3.resource('s3', region_name='us-east-1')
s3.create_bucket(Bucket="inputbucket")
s3.create_bucket(Bucket="outputbucket")

current_time = datetime.now().strftime("%H:%M:%S")

def whichcall(input_str):
    inputsize = getsizeof(input_str)
    if inputsize < 5000:
        return True
    return False
    
def countsplits(input_str):
    inputsize = getsizeof(input_str)
    if inputsize > 5000:
        splits = math.ceil(inputsize/5000)
        if splits > 25:
            raise("This text is too large for analysis. Please try something else.")
    return splits
    
def tokenizetext(input_str):
    sent_tokens = sent_tokenize(input_str)
    num_sent = len(sent_tokens)
    if num_sent > 25:
        raise("This text is too large for analysis. Please try something else.")
    str_sizes = []
    for s in sent_tokens:
        str_sizes.append(getsizeof(s))
        if str_sizes[-1] > 5000:
            raise("This sentence is too large for analysis")
        continue
    return sent_tokens
    

def lambda_handler(event, context):
    
    response = event['text']
    s3_client.put_object(Body=response, Bucket=bucket1, Key=current_time+".txt")
    
    if whichcall(response):
        print("Less than 5000 bytes. Use normal detect sentiment call")
        sentiment = client.detect_sentiment(Text=response, LanguageCode='en')
        resp_sent = sentiment['Sentiment']
        sent_score = sentiment['SentimentScore'] #dict with probabilities for each sentiment: MIXED, NEGATIVE, NEUTRAL, POSITIVE
        
    else:
        print("Text larger than 5000 bytes. Use batch detect sentiment call")
        sent_list = tokenizetext(reponse)
        results = client.batch_detect_sentiment(TextList=sent_list, LanguageCode='en')
        results = results['ResultList']
        scores = [result['SentimentScore'] for result in results] #list of dictionaries with probabilities for each sentiment
        num_scores = len(scores)
        score = dict(
            'POSITIVE': sum(value for key, value in scores.items() if key == 'POSITIVE'),
            'NEGATIVE': sum(value for key, value in scores.itens() if key == 'NEGATIVE'),
            'NEURAL': sum(value for key, value in scores.items() if key == 'NEURAL'),
            'NEGATIVE': sum(value for key, value in scores.items() if key == 'NEGATIVE'))
        score = dict(key: (score[key] / num_scores) for key in score.keys())
        print(score)
        
    s3_client.put_object(Body=score, Bucket=bucket2, Key=current_time+".txt")
        
        
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': score
    }
