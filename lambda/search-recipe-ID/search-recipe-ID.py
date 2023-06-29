import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    user_message = event['queryStringParameters']['q']
    print("DEBUG: user_message:", user_message) # 632071

    query_id = user_message
    queried_recipe = dynamodb_search(query_id)
    
 
    return {
        'statusCode': 200,
        'headers': { 
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps({
            "results": queried_recipe
        })
    }
    
# # THE RETURNED VALUE For Spoonacula
# {
#     "results": {
#         "instructions": "<ol><li>Heat the olive oil in a large skillet. Add in minced garlic, shallots, and green bell pepper.  Stir until fragrant and tender, about 3 minutes. Season it with salt and black pepper.</li><li>Add the ground beef to the vegetables. Stir and cook about 5 minutes, until the meat is no longer pink and fully cooked. Add tomato sauce, barbecue sauce, Worcestershire, and hot sauce into the skillet. Stir to combine. Simmer until thickened.</li><li>To serve, spoon and pile sloppy meat onto the toasted, buttered bun bottoms and cover with bun tops with your favourite side dish or pickles.</li></ol>",
#         "ingredients": [
#             "100 grams American barbecue sauce",
#             "4 Homemade burger buns, split, toasted, and buttere",
#             "2 Garlic cloves, minced",
#             "1/2 Green bell pepper, diced",
#             "450 grams Ground beef",
#             "1 teaspoon Hot sauce",
#             "1 tablespoon Olive oil",
#             "Salt and freshly ground black pepper",
#             "2 Shallots, chopped",
#             "180 grams Tomato sauce",
#             "2/3 tablespoon Worcestershire sauce"
#         ],
#         "id": "632071",
#         "image": "https://spoonacular.com/recipeImages/632071-556x370.jpg",
#         "title": "All American Sloppy Joes"
#     }
# }


def dynamodb_search(query_id):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table_db = dynamodb.Table('recipes')
    
    scanresult = table_db.query(KeyConditionExpression=Key('id').eq(query_id))
    recipe = scanresult['Items'][0]
    
    return recipe
