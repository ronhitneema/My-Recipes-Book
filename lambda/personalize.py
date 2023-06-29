import json
import boto3
from boto3.dynamodb.conditions import Key


CAMPAIGN_ARN = 'arn:aws:personalize:us-east-1:522843601067:campaign/campaign2again'
TABLE_NAME = 'recipes'

personalizeRt = boto3.client('personalize-runtime')


# Get recommendations for a given user
def recommendations_for(username):
    response = personalizeRt.get_recommendations(
        campaignArn = CAMPAIGN_ARN,
        userId = username,
        numResults = 10
    )

    recommended_recipes = []
    for item in response['itemList']:
        recommended_recipes.append(item['itemId'])

    return recommended_recipes
    # https://docs.aws.amazon.com/personalize/latest/dg/getting-real-time-recommendations.html#recommendations


# Query DynamoDB to get recipe details
def query_database(recipe_id):
    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table(TABLE_NAME)
    response = dynamoTable.query(
        KeyConditionExpression=Key('id').eq(recipe_id)
    )
    return response['Items']
    # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html


def lambda_handler(event, context):
    print("EVENT", event)

    USER = event['queryStringParameters']['q']
    print('USER', USER)

    # Get recommendations from Personalize
    recs_for_user = recommendations_for(USER)

    print("RECOMMENDATIONS ---> ", recs_for_user)

    recipe_details = []
    for recipe_id in recs_for_user:
        print("RECIPE ID", recipe_id)
        recipe_details.append(query_database(recipe_id))

    print("RECIPE DETAILS ---> ", recipe_details)
    print('tyepofrecipedetails', type(recipe_details))


    return {
        "statusCode": 200,
        'headers': {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(recipe_details)
        # "isBase64Encoded": true|false,
    }
