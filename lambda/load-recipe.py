import json
import boto3
from boto3.dynamodb.conditions import Key

region = 'us-east-1'

def lambda_handler(event, context):

    print("DEBUG:", event)
    query_id = event['queryStringParameters']['id']
    print('queryStringParameters', query_id)

    #get UserName from Parameter
    #query_id = '1000566'
    print(f'Recipes from {query_id}')

    recipeDetails = dynamodb_recipe_search(query_id)
    # recipe = {
    #         "id": recipeDetails['id'],
    #         "title": recipeDetails['title'],
    #         "image": recipeDetails['image'],
    #         "instructions": recipeDetails['instructions'],
    #         "ingredients": recipeDetails['ingredients']
    #     }

    print("DEBUG: ", recipeDetails)

    return {
        'statusCode': 200,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(recipeDetails)
    }

def dynamodb_recipe_search(recipeId):
    dynamodb = boto3.resource('dynamodb', region_name = region)
    table_db = dynamodb.Table('recipes')

    queryRecipeResult = table_db.query(KeyConditionExpression=Key('id').eq(str(recipeId)))
    item = queryRecipeResult['Items'][0]
    return (item)
