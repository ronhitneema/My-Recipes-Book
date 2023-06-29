import json
import boto3
from boto3.dynamodb.conditions import Key

region = 'us-east-1'

def lambda_handler(event, context):

    print("DEBUG:", event)
    query_user = event['queryStringParameters']['userfav']
    print('queryStringParameters', query_user)

    #get UserName from Parameter test
    # query_user = 'bornita'
    # print(f"Recipes from {query_user}")


    #get total recipes of User
    recipes = query_user_recipe(query_user)

    listRecipesOfUser = []

    #get list of recipe details
    for recipe in recipes:
        print(recipe['username'], ":", recipe['savedrecipes'])
        fav_recipe_count = len(recipe['savedrecipes'])
        print(f"Fav'd Recipes Count {fav_recipe_count}")

        fav_recipe_arr = recipe['savedrecipes']

        #select recent 2 recipes for profile page
        if fav_recipe_count > 2:
            fav_recipe_arr =  recipe['savedrecipes'][-2:]
        print(f"Recent Fav'd Recipes: {fav_recipe_arr}")

        for recipeid in fav_recipe_arr:

            print ("DEBUG Adding fav to list", recipeid)
         ## add code to create another search and add to an List
            recipeDetails = dynamodb_recipe_search(recipeid)
            bundle = {
                "id": recipeid,
                "title": recipeDetails['title'],
                "image": recipeDetails['image'],
                "recipe_count": fav_recipe_count
            }

            #print ("DEBUG :", bundle)

            listRecipesOfUser.append(bundle);


    print(f"All Recent Fav'd Recipes Listed: {listRecipesOfUser}")

    return {
        'statusCode': 200,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(listRecipesOfUser)
    }

def query_user_recipe(userName, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name = region)

    table = dynamodb.Table('Users')
    response = table.query(
        KeyConditionExpression=Key('username').eq(userName)
    )
    #print("DEBUG Users: ",response['Items'])
    return response['Items']

def dynamodb_recipe_search(recipeId):
    dynamodb = boto3.resource('dynamodb', region_name = region)
    table_db = dynamodb.Table('recipes')

    queryRecipeResult = table_db.query(KeyConditionExpression=Key('id').eq(str(recipeId)))
    #print("DEBUG queryRecipeResult:", queryRecipeResult)
    item = queryRecipeResult['Items'][0]

    #print(item['title'], ":", item['image'])
    return (item)
