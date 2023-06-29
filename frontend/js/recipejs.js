var apigClient = apigClientFactory.newClient()
var sPageURL = window.location.search.substring(1)
var id = sPageURL.split('=')[1] //"632071"

let data = {
    UserPoolId: config.cognito.userPoolId,
    ClientId: config.cognito.clientId
}
console.log("DATA", data)
let CognitoUserPool = AmazonCognitoIdentity.CognitoUserPool
let userPool = new AmazonCognitoIdentity.CognitoUserPool(data)
var cognitoUser = userPool.getCurrentUser()
console.log("cognito user", cognitoUser)

if (cognitoUser == null) {
    $('#save-recipe-button').attr('hidden', true)
    $('#add-recipe-nav-button').attr('hidden', true)
    $('#recommendations-nav-button').attr('hidden', true)
    $('#bartor-nav-button').attr('hidden', true)
}

function signOut() {
    if (cognitoUser != null) {
        cognitoUser.signOut();
        window.open("login.html", "_self");
    }
}


function isAlpha(str) {
    return /^[a-zA-Z]+$/.test(str)
}

var userName = ""
var idStart = 0
if (isAlpha(id[0])) {
    for (var i = 0; i < id.length; i++) {
        if (!isAlpha(id[i])) {
            idStart = i
            break
        }
    }
    userName = id.substring(0, idStart)
}
console.log("userName")
console.log(userName)



searchRecipe(id)

function searchRecipe(id) {
    var params = { q: id }
    var body = {}
    var additionalParams = {}
    searchResults = []

    return apigClient.searchGet(params, body, additionalParams)
        .then(function (result) {
            if (userName != "") {
                $('#user-name-link').html(userName)
            } else {
                $('#user-name-row').attr('hidden', true)
            }


            var title = result.data.results.title //string
            var image = result.data.results.image //http string
            var ingredients = result.data.results.ingredients //array
            var instructions = result.data.results.instructions //html string

            $('#top-title').html(title + " | Recipe Book")
            $('#recipe-title').html(title)
            if (image != "No Image" && image != "") {
                $('#recipe-image').attr('src', image)
            }

            //output ingredients
            for (var i = 0; i < ingredients.length; i++) {
                var currLine = ingredients[i]
                var descStart = 0

                for (var j = 0; j < currLine.length; j++) {
                    if (isAlpha(currLine[j])) {
                        descStart = j
                        break
                    }
                }

                var quant = ""
                if (descStart != 0) {
                    quant = currLine.substring(0, descStart - 1).trim()
                }
                var desc = currLine.substring(descStart, currLine.length).trim()

                $('#ingredients-one-by-one').append('<dt>' + quant + '</dt><dd>' + desc + '</dd>')
            }

            //output instructions
            if (instructions.startsWith('<')) {
                $('#directions-step').append(instructions)
            }
            else {
                var instructionsList = instructions.split(/\r?\n/)
                var newInstruction = ""
                for (var i = 0; i < instructionsList.length; i++) {
                    if (instructionsList[i].trim() != "") {
                        newInstruction += '<li>' + instructionsList[i] + '</li>'
                    }
                }
                newInstruction = '<ol>' + newInstruction + '</ol>'

                $('#directions-step').append(newInstruction)
            }

        })
        .catch(function (error) {
            console.log("DEBUG: error result")
            console.log(error)
            alert("Something went Wrong!")
        })
}


function saveReciepe() {
    console.log('Saving recipe')

    console.log('recipeID: ' + id)
    console.log('user: ' + cognitoUser)

    let params = {
        "Content-Type": "multipart/form-data"
    }
    let body = {
        "username": cognitoUser,
        "recipeID": id
    }
    let additionalParams = {}

    return apigClient.uploadPut(params, body, additionalParams)
        .then(function (result) {
            console.log(result)
            alert("Really successfully saved the recipe!")
        })
        .catch(function (error) {
            console.log("DEBUG: the error result")
            console.log(error)
            alert("Successfully saved the recipe!")
            // alert("Something went Wrong!")
        })
}