import json
import boto3
import datetime
import requests
# from requests_aws4auth import AWS4Auth
import spoonacular as sp


# def lambda_handler(event, context):
api = sp.API("43ebbf5785aa40b0a6777bf4349bde6c")

resultData = []

response = api.get_random_recipes(number=1)
message = response.json()
result = message['recipes']
print(result)
# for i in result:
#     ingredients = []
#     tags = i['tags']
#     id = i['id']
#     title = i['title']
#     instructions = i['instructions']
#     if 'image' in i:
#         image = i['image']
#     test = i['extendedIngredients']
#     for i in test:
#         ingredients.append(i['original'])
#     if 'image' in i:
#         resultData.append([id, title, ingredients, instructions, tags, image])
#     else:
#         resultData.append([id, title, ingredients, instructions, tags, 'No Image'])

    # # # Add data to DynamodDB
    # dynamoInsert(resultData)
    #
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('success')
    # }


def dynamoInsert(recipe):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('recipes')

    for i in recipe:
        tableEntry = {
            'id': i[0],
            'title': i[1],
            'ingredients': i[2],
            'instructions': i[3],
            'image': i[4]
        }

        table.put_item(
            Item={

                'id': str(tableEntry['id']),
                'title': tableEntry['title'],
                'ingredients': tableEntry['ingredients'],
                'instructions': tableEntry['instructions'],
                'image': tableEntry['image']
            }
        )