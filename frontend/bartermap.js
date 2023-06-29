window.onload = getUser

var buyerId = "";
function getUser() {
    // Get user data from Cognito
    let data = {
        UserPoolId: config.cognito.userPoolId,
        ClientId: config.cognito.clientId
    };

    let CognitoUserPool = AmazonCognitoIdentity.CognitoUserPool;
    let userPool = new AmazonCognitoIdentity.CognitoUserPool(data);
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
    buyerId = username

    markerDetails(params,body,additionalParams)
}

async function markerDetails(params, body, additionalParams) {

    // Connect to API Gateway
    let apigClient = apigClientFactory.newClient();
    console.log("apigClient", apigClient);

    try {
        // API GATEWAY
        const getresponse = await apigClient.rootGet(params, body, additionalParams);

        if (getresponse) {
            console.log("RESPONSE", getresponse)
            let geojson = getresponse.data;
            mapboxgl.accessToken = 'pk.eyJ1IjoiYmVuamk3ODkwIiwiYSI6ImNrb2x2NnF1NDIxNzAydnB3dGlrczF6d24ifQ.U4UVnWoUly_S7eX0ughcKA';
            var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-73.9592492763008,40.722485940954854],
            zoom: 12
          });
            // add markers to map
            geojson.features.forEach(function (marker) {
                // create a HTML element for each feature
                var el = document.createElement('div');
                el.className = 'marker';

                console.log(marker.geometry.coordinates)
                // make a marker for each feature and add it to the map
                new mapboxgl.Marker(el)
                    .setLngLat(marker.geometry.coordinates)
                    .setPopup(
                        new mapboxgl.Popup({offset: 25}) // add popups
                            .setHTML(
                                '<h5>' +'</h5><a href="https://dch04u22l9237.cloudfront.net/recipe.html?id=' + marker.properties.recipe_id + '"><h4>' +marker.properties.title +'</h4></a>'
                                + '<img src="'+ marker.properties.image +'" style="width:150px;height:100px;">'
                                // + '<h6> User: '+ marker.properties.user+'</h6>'
                                +'<button onclick="sendSMS(\''+marker.properties.user +'\')"> Contact '+marker.properties.user +' to barter!</button>'
                            )
                    )
                    .addTo(map);
            });
        }

    } catch (error){
        console.log("Error", error);
    }
}

function sendSMS(sellerId){

    console.log('Sending SMS')
    console.log("seller", sellerId)
    console.log("buyer", buyerId)
    sendSMSPUT(sellerId, buyerId)
}

// Uploading recipe via API /PUT method
async function sendSMSPUT(sellerId, buyerId) {

    console.log("Step 1");

    // Connect to API Gateway
    let apigClient = apigClientFactory.newClient();
    console.log("apigClient", apigClient);

    let params = {
        "buyerId": buyerId,
        "sellerId": sellerId
    };
    
    let body = {};
    let additionalParams = {};

    // API GATEWAY
    apigClient.markerPut(params, body, additionalParams);
    console.log("Sent to Put")
    alert("We've sent a SMS to " + sellerId + " with your contact details.")
}
