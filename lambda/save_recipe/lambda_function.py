import json
import boto3
import datetime
import csv


REGION = 'us-east-1'
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    infoString = event['body'] 
    info = json.loads(infoString)
    
    username = info['username']['username']
    recipeID = info['recipeID']
    print("DEBUG username:", username)
    print("DEBUG recipeID:", recipeID)
    
    dynamodb = boto3.resource('dynamodb', region_name = REGION)
    table = dynamodb.Table('Users')
    
    result = table.update_item(
        Key={
            'username': username
        },
        UpdateExpression="SET savedrecipes = list_append(if_not_exists(savedrecipes, :empty_list), :id)",
        ExpressionAttributeValues={
            ':id': [recipeID],
            ':empty_list': []
        },
    )
    


    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('in success')
        return {
            'statusCode': 200,
            'body': json.dumps('success')
        }
