import json
import boto3
from boto3.dynamodb.conditions import Key

region = 'us-east-1'

def lambda_handler(event, context):

    print("DEBUG:", event)
    query_user = event['queryStringParameters']['username']
    print('queryStringParameters', query_user)

    #get UserName from Parameter
    #query_user = 'bornita'
    print(f"Recipes from {query_user}")


    #get total recipes of User
    recipes = query_user_recipe(query_user)
    recipe_count = len(recipes)
    print(f"Recipes Count {recipe_count}")

    #select recent 2 recipes for profile page
    if recipe_count > 2:
       recipes =  recipes[-2:]

    listRecipesOfUser = []

    #get list of recipe details
    for recipe in recipes:
        print(recipe['userName'], ":", recipe['recipeId'])
         ## add code to create another search and add to an List
        recipeDetails = dynamodb_recipe_search(recipe['recipeId'])
        bundle = {
            "id": recipe['recipeId'],
            "title": recipeDetails['title'],
            "image": recipeDetails['image'],
            "recipe_count": recipe_count
        }

        print ("DEBUG :", bundle)

        listRecipesOfUser.append(bundle);

        #listRecipesOfUser.append([recipeDetails['title'],recipeDetails['image'],recipe_count])
        #listRecipesOfUser.append([recipe['userName'],recipeDetails['title'],recipeDetails['image']])

    print(f"All Recipes Listed: {listRecipesOfUser}")

    return {
        'statusCode': 200,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(listRecipesOfUser)
    }

def query_user_recipe(userName, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name = region)

    table = dynamodb.Table('recipesOfUser')
    response = table.query(
        KeyConditionExpression=Key('userName').eq(userName)
    )
    #print("DEBUG recipeOfUsers: ",response['Items'])
    return response['Items']

def dynamodb_recipe_search(recipeId):
    dynamodb = boto3.resource('dynamodb', region_name = region)
    table_db = dynamodb.Table('recipes')

    queryRecipeResult = table_db.query(KeyConditionExpression=Key('id').eq(str(recipeId)))
    #print("DEBUG queryRecipeResult:", queryRecipeResult)
    item = queryRecipeResult['Items'][0]

    #print(item['title'], ":", item['image'])
    return (item)
