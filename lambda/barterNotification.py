import boto3
import json
from boto3.dynamodb.conditions import Key

region = "us-east-1"

def lambda_handler(event, context):

    # seller_id = 'benteo'
    # buyer_id = 'benji7890'

    print("DEBUG:", event)
    buyer_id = event['queryStringParameters']['buyerId']
    seller_id = event['queryStringParameters']['sellerId']
    print('queryStringParameters', buyer_id, seller_id)


    try:

        sms_message = None

        # get recipe of seller
        seller_dish = dynamodb_barter_search(seller_id, buyer_id, 'sell')
        phone = seller_dish['phone']
        phoneNumber = '+1'+ str(phone)
        print("DEBUG: sms-phone", phoneNumber)

        # get recipe of buyer
        buyer_dish = dynamodb_barter_search(seller_id, buyer_id, 'buy')
        b_phone = buyer_dish['phone']
        buyerPhone = '+1'+ str(b_phone)
        #print("DEBUG: buyerPhone", buyerPhone)

        #get recipe name of seller
        seller_dish_details = dynamodb_recipe_search(seller_dish['recipe_id'])
        sell_dish_name = seller_dish_details['title']

        #get recipe name of buyer
        buyer_dish_details = dynamodb_recipe_search(buyer_dish['recipe_id'])
        buy_dish_name = buyer_dish_details['title']

        #recipe link cloudfront
        currAnchor = "https://dch04u22l9237.cloudfront.net/recipe.html?id=" + buyer_dish['recipe_id']

        sms_message = F'Hello! {buyer_id} wants to barter your {sell_dish_name} dish. Check out his/her dish {buy_dish_name} here {currAnchor}.\n' + F'Contact: {buyerPhone}\n'+'Keep Bartering!'
        print(sms_message)


        #publish sms through sns clients
        sns = boto3.client("sns", region_name= region)

        response = sns.publish(PhoneNumber=phoneNumber, Message=sms_message)
        print(response)
        msg ='SMS sent!'

    except:
        print('DEBUG:','No msg created.')
        msg = 'No msg created.'
       #print('DEBUG:',response)

    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }

def dynamodb_recipe_search(recipeId):
    dynamodb = boto3.resource('dynamodb', region_name = region)
    table_db = dynamodb.Table('recipes')

    queryRecipeResult = table_db.query(KeyConditionExpression=Key('id').eq(str(recipeId)))
    item = queryRecipeResult['Items'][0]
    print("DEBUG: Recipe query", item)
    return (item)

def dynamodb_barter_search(seller_id, buyer_id,flg):
    dynamodb = boto3.resource('dynamodb', region_name = region)
    table_db = dynamodb.Table('barter')

    user = buyer_id

    if flg == 'sell' :
        user = seller_id

    queryBarter = table_db.query(KeyConditionExpression=Key('username').eq(str(user)))
    item = queryBarter['Items'][0]
    print("DEBUG: Barter query", item)
    return (item)
