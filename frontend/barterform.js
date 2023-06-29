window.onload = getUser

function getUser(){
    // Get user data from Cognito
    let data = {
        UserPoolId: config.cognito.userPoolId,
        ClientId: config.cognito.clientId
    };

    let CognitoUserPool = AmazonCognitoIdentity.CognitoUserPool;
    let userPool =  new AmazonCognitoIdentity.CognitoUserPool(data);
    let cognitoUser = userPool.getCurrentUser();

    let username;
    if (cognitoUser) {
        username = cognitoUser.username
    } else {
        username = ''
    }

    console.log("USERNAME", username)

    var params = {q: username};
    var body = {
        "username": username,
    };
    var additionalParams = {};

    // let apigClient = apigClientFactory.newClient();
    // console.log("apigClient", apigClient);

    // apigClient.idGet(params, body, additionalParams);
    userAPI(params,body,additionalParams)
    document.getElementById('username').value = document.getElementById('username').text = username

    }

async function userAPI(params, body, additionalParams) {

    // Connect to API Gateway
    let apigClient = apigClientFactory.newClient();
    console.log("apigClient", apigClient);

    try {
        // API GATEWAY
       const getresponse = await apigClient.userGet(params, body, additionalParams);
       if (getresponse) {
           console.log("RESPONSE", getresponse)
           let recipesList = getresponse.data;
           console.log("RECIPES LIST", recipesList)

       var select = document.getElementById("recipes");

       for (i=0; i<recipesList.length; i++) {
           let recipeTitle = recipesList[i]['title'] + ' ' + recipesList[i]['id']
           var option = document.createElement('option');
           option.text = option.value = recipeTitle;
           select.add(option, 0);
           console.log(recipeTitle)
       }

       }
    } catch (error) {
        console.log("Error", error);
    }
}

// Function to add new recipes
// ---------------------------------------------------------------------------------------
function addBarter(e){
    e.preventDefault();
    console.log('Add New Barter')

    const recipe = document.getElementById("recipes").value
    const username = document.getElementById("username")
    const date = document.getElementById("date").value
    const comments = document.getElementById("comments").value
    const phone = document.getElementById("phone").value
    const address = document.getElementById("address").value
    const city = document.getElementById("city").value
    const state = document.getElementById("state").value
    const zip = document.getElementById("zip").value

    console.log("FORM DETAILS", username, name, date, comments, phone, address, city, state, zip)

    // Uploading recipe via API /PUT method
    async function addBarterPUT() {
        e.preventDefault();
        console.log("Submit clicked...");

        // Connect to API Gateway
        let apigClient = apigClientFactory.newClient();
        console.log("apigClient", apigClient);

        let params = {
            "Content-Type": "multipart/form-data"
        };
        let body = {
              'recipes': recipe,
              'username': username,
              'date': date,
              'comments': comments,
              'phone': phone,
              'address': address,
              'city': city,
              'state': state,
              'zip': zip
        };
        let additionalParams = {};

        // API GATEWAY
        apigClient.uploadPut(params, body, additionalParams);

        document.getElementById('barter-form').reset()
        alert('Barter Form has been submitted!')
        // document.location.href="barter.html"
    }

    addBarterPUT()
}


//
// const barterTable = 'barter';
//
// //insert pool id of your congito pool
// const IdentityPoolId = 'us-east-1:561ca273-9c58-4922-91f0-ba746a6023b4';
// const credentials = new AWS.CognitoIdentityCredentials({ IdentityPoolId });
// //insert your region
// const region = 'us-east-1';
//
// AWS.config.update({
//   region,
//   credentials
// });
//
// const ddb = new AWS.DynamoDB({
//   apiVersion: '2012-10-08'
// });
//
// function addBarter() {
//   const username = document.getElementById("username").value
//   const name = document.getElementById("name").value
//   const date = document.getElementById("date").value
//   const comments = document.getElementById("comments").value
//   const phone = document.getElementById("phone").value
//   const email = document.getElementById("email").value
//   const address = document.getElementById("address").value
//   const zip = document.getElementById("zip").value
//   const params = {
//     "RequestItems": {
//       "barter": [
//         {
//           "PutRequest": {
//             "Item": {
//               'username': {"S": username},
//               'name': {"S": name},
//               'date': {"S": date},
//               'comments': {"S": comments},
//               'phone': {"S": phone},
//               'email': {"S": email},
//               'address': {"S": address},
//               'zip': {"S": zip},
//               // 'createdAt': {"N": Date.now().toString()}
//             }
//           }
//         }
//       ]
//     }
//   }
//   ddb.batchWriteItem(params, function(err, data) {
//     if (err) {
//       return alert('Error: ' + err.message);
//     } else {
//       document.getElementById('barter-form').reset()
//     }
//   })
// }
