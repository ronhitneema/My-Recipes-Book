import json
import datetime
import time
import os
import dateutil.parser
import logging
import boto3
import random
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# ElasticSearch Instance
host = 'search-recipes-2i7rrbbths6vftpgij7o44u7mu.us-east-1.es.amazonaws.com'
region = 'us-east-1'
TABLE_NAME = 'recipes'

def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    print("EVENT", event)

    text = event['queryStringParameters']['q']
    print('TEXT', text)

    # Call Lex Chatbot
    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='searchBot',
        botAlias='prod',
        userId='user',
        inputText=text #send user input to lex chatbot
    )

    print("RESPONSE FROM LEX", response)


    # Handle invalid user searches
    if 'slots' not in response or 'food' not in response['slots'] or response['slots']['food'] is None:
        return {
            "statusCode": 200,
            'headers': {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps([])
        }


    # Extract labels
    food_search = response['slots']['food']
    food_search2 = response['slots']['secondfood']

    print("SEARCH FOOD", food_search)
    print("SECOND FOOD", food_search2)


    # ElasticSearch auth
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # Connect to ElasticSearch
    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    # https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-request-signing.html#es-request-signing-python


    searchresults = []

    # Search function
    def elasticsearch_helper(labelname):
        search_res = es.search(index="recipes", body={"query": {"match": {'labels': labelname}}})
        print('SEARCH RES', search_res)
        for hit in search_res['hits']['hits']:
            searchresults.append(hit['_id'])
    # https://elasticsearch-py.readthedocs.io/en/v7.11.0/


    # Call search function
    searchquery = [food_search, food_search2] if food_search2 else [food_search]
    for i in searchquery:
        elasticsearch_helper(i)
    print('SEARCH RESULTS', searchresults)

    # Remove duplicate files
    unique_results = list(set(searchresults))
    # prevent too many reads from DB
    if len(unique_results) > 10:
        selected = random.sample(unique_results,10)
    else:
        selected = unique_results
    print("UNIQUE RESULTS", unique_results)

    # Query DynamoDB to get recipe details
    def query_database(recipe_id):
        dynamodb = boto3.resource('dynamodb')
        dynamoTable = dynamodb.Table(TABLE_NAME)
        response = dynamoTable.query(
            KeyConditionExpression=Key('id').eq(recipe_id)
        )
        return response['Items']
    # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html

    recipe_details = []
    for recipe_id in selected:
        print("RECIPE ID", recipe_id)
        recipe_details.append(query_database(recipe_id))

    print("RECIPE DETAILS ---> ", recipe_details)
    print("RECIPE IDs", selected)

    return {
        "statusCode": 200,
        'headers': {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(recipe_details)
    }
