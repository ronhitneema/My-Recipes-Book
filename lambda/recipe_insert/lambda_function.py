import json
import boto3
import spoonacular as sp
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import re

#############################static variables#############################
REGION = 'us-east-1'
# SPOONACULAR_API = '43ebbf5785aa40b0a6777bf4349bde6c' #ben's account
# SPOONACULAR_API = 'e949bb1de19346d380848fb8487336a1' #jin's account
SPOONACULAR_API = '00ed6504e3a44f528d40888fa604e729' #claudia's account


#############################ES credentials#############################
credentials = boto3.Session().get_credentials()
service = 'es'
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, REGION, service, session_token=credentials.token)


def lambda_handler(event, context):
    api = sp.API(SPOONACULAR_API)
    
    response = api.get_random_recipes(number = 150)
    response_json = response.json()
    recipes_arr = response_json['recipes']
    # print("DEBUG recipes_arr:", recipes_arr)
#   {
#       "recipes":[
#           {/* recipe data as in Get Recipe Information endpoint */}
#      ]
#   }
    
    # Add data to DynamodDB
    dynamoInsert(recipes_arr)

    # # Add index data to the ElasticSearch
    addElasticIndex(recipes_arr)   
        
    return {
        'statusCode': 200,
        'body': json.dumps('success')
    }


def dynamoInsert(recipes_arr):
    dynamodb = boto3.resource('dynamodb', region_name = REGION)
    table = dynamodb.Table('recipes')


    for recipe in recipes_arr:
        # get ingredients
        ingredients = []
        for extendedIngredient in recipe['extendedIngredients']:
            ingredients.append(re.sub('[æÄìº¬Ω]', '', extendedIngredient['original']))
            
        # get image
        if 'image' in recipe:
            image = recipe['image']
        else:
            image = 'No Image'
            
            
        tableEntry = {
            'id': recipe['id'],
            'title': re.sub('[æÄìº¬Ω]', '', recipe['title']),
            'ingredients': ingredients,
            'instructions': re.sub('[æÄìº¬Ω]', '', recipe['instructions']),
            'image': image
        }
        print("DEBUG tableEntry:", tableEntry)


        table.put_item(
            Item={
                'id': str(tableEntry['id']),
                'title': tableEntry['title'],
                'ingredients': tableEntry['ingredients'],
                'instructions': tableEntry['instructions'],
                'image': tableEntry['image']
            }
        )

def addElasticIndex(recipes_arr):
    es_endpoint = 'search-recipes-2i7rrbbths6vftpgij7o44u7mu.us-east-1.es.amazonaws.com' 
    
    es = Elasticsearch(
        hosts = [{'host': es_endpoint, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    for recipe in recipes_arr:
        labels = []
        labels += recipe['cuisines'] # ["American"]

        newTitle = ""
        for char in recipe['title']: # "Pasta with Garlic, Scallions, Cauliflower & Breadcrumbs"
            if char.isalnum() or char == ' ':
                newTitle += char
        labels += newTitle.split()    
        
        labels += recipe['dishTypes'] # ["lunch","main course","main dish","dinner"]
        
        for ingredientDetails in recipe['extendedIngredients']:
            labels.append(ingredientDetails['name'])
        
        finalLabels = []
        dontInclude = ['and', 'with']
        for label in labels: 
            if len(label) > 1 and label not in dontInclude: # only words longer than 1 alphabet
                finalLabels.append(label.lower()) # make everything to lowercase
             
        index_data = {
            'id': recipe['id'],
            'labels': finalLabels
        }

        print("DEBUG index_data:", index_data)

        es.index(index="recipes", id=recipe['id'], body=index_data, refresh=True, request_timeout=30) # NEED TO CHECK IF THIS WORKS SO THAT SEARCH IN THE ES WORKS FINE