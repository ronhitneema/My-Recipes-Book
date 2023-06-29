import json
import json
import boto3
from boto3.dynamodb.conditions import Key
from geopy.geocoders import Nominatim


region = 'us-east-1'

def lambda_handler(event, context):


    print("DEBUG:", event)

    #find barter submitted by the user
    barters = dynamodb_barter_search()

    #list of features
    features = []

    #add barters to List
    for barter in barters:
        print(barter['username'], ":", barter['recipe_id'])
        recipe = dynamodb_recipe_search(barter['recipe_id'])
        point = generate_coordinates(barter['address'])

        struct = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": point
                    },
                    "properties": {
                        "title": recipe['title'],
                        "user":  barter['username'],
                        "image": recipe['image'],
                        "recipe_id": barter['recipe_id']
                    }
                }
        features.append(struct);

        #print ("DEBUG :", properties)


    geoJson = {
                "type": "FeatureCollection",
                "features":features
            }

    return {
        'statusCode': 200,
        'headers': {"Access-Control-Allow-Origin": "*"},
        'body': json.dumps(geoJson)
    }

# query barter table for the logged in user
def dynamodb_barter_search():
    dynamodb = boto3.resource('dynamodb', region_name = region)
    table_db = dynamodb.Table('barter')

    #queryBarterResult = table_db.query(KeyConditionExpression=Key('username').eq(str(user)))
    #print("DEBUG queryBarterResult:", queryBarterResult)
    #item = queryBarterResult['Items'][0]

    scanBarter = table_db.scan()
    items = scanBarter['Items']

    return items

def dynamodb_recipe_search(recipeId):
    dynamodb = boto3.resource('dynamodb', region_name = region)
    table_db = dynamodb.Table('recipes')

    queryRecipeResult = table_db.query(KeyConditionExpression=Key('id').eq(str(recipeId)))
    #print("DEBUG queryRecipeResult:", queryRecipeResult)
    item = queryRecipeResult['Items'][0]
    return (item)

def generate_coordinates(address):
    #get coordinates
    print(address)
    geolocator = Nominatim(user_agent="gather app")

    data = geolocator.geocode(address, timeout=1000)
    point = []
    point.append(data.point.longitude)
    point.append(data.point.latitude)
    #print("COORD: ", point)
    return point


