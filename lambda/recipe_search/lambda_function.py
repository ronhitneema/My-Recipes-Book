import json
import boto3
from boto3.dynamodb.conditions import Key
from random import randint
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


credentials = boto3.Session().get_credentials()
region = 'us-east-1'
service = 'es'
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


def dynamodb_search(rand_recipe_id):
    dynamodb = boto3.resource('dynamodb', region_name = region)
    table_db = dynamodb.Table('recipes')

    scanresult = table_db.query(KeyConditionExpression=Key('id').eq(str(rand_recipe_id)))
    print("DEBUG scanresult:", scanresult)
    item = scanresult['Items'][0]

    title = item['title']
    image = item['image']
    ingredients = item['ingredients']
    instructions = item['instructions']
    
    return (title, image, ingredients, instructions)
    
def rand_elastic_search(keyword):
    es_endpoint = 'search-recipes-2i7rrbbths6vftpgij7o44u7mu.us-east-1.es.amazonaws.com' 
    
    es = Elasticsearch(
        hosts = [{'host': es_endpoint, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    # Get the food category from queue message attributes.
    es_search_result = es.search(index = "recipes", body = {
        "query": {
            'match': {
                'labels': keyword
            }}})
    
    print("DEBUG es_search_result:", es_search_result)
  
    
    # Choose random among returned list
    total_num_searches = len(es_search_result['hits']['hits'])
    if total_num_searches == 0:
        return [f'Sorry! We do not have any recipe for {keyword}.']

    rand_idx = randint(0,total_num_searches - 1)
    rand_recipe_id = es_search_result['hits']['hits'][rand_idx]['_source']['id']
    
    return rand_recipe_id



def lambda_handler(event, context):
    
    print("DEBUG event:", event) # 'queryStringParameters': {'q': 'apple'} # will need to set up the API Gateway to get this kind of query
    # this is smiliar to GET of Assginment 2
    user_message = event['queryStringParameters']['q'].lower() # 'apple' # to lowercase
    # have the query message to be trimmed and lowercased in frontend javascript (ex.document.getElementById("XXXX").value.trim().toLowerCase())

    if user_message == None:
        return{
            'statusCode': 200,
            'headers': { 
                'Access-Control-Allow-Headers' : 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body':json.dumps("No Message!")
        }

    # dont put lex here as we did on assignment 2 (MAY CHANGE)
    
    rand_recipe_id = rand_elastic_search(user_message)
    title, image, ingredients, instructions = dynamodb_search(rand_recipe_id)
    print("DEBUG title, image, ingredients, instructions:", title, image, ingredients, instructions)