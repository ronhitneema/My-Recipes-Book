window.onload = loadProfile

//call API get recipes for this user

function loadProfile() {
    //pass username to API
    let user = document.getElementById("username").innerHTML;
    console.log("Loading User: ", user);

    if (user===''){
     window.open("login.html","_self")
    }
    else{

        var params = {username: user};
        var body = {};
        var additionalParams = {};

        userAPI(params, body, additionalParams);

        var params1 = {userfav: user};
        var body1 = {};
        var additionalParams1 = {};

        favRecipeAPI(params1, body1, additionalParams1);
    }

}

function loadRecipe(id){
//   localStorage.setItem("recipe_key",id);
//   window.open("recipe.html");
   let redirect_link = "https://dch04u22l9237.cloudfront.net/recipe.html?id=" + id;
//   alert(id);
//   alert(redirect_link);
   window.open(redirect_link);
}

function loadForm(id){
   localStorage.setItem("form_key",id);
   window.open("barter_form.html");
}


// Load Profile using API /GET method
async function userAPI(params, body, additionalParams){

    // Connect to API Gateway
    let apigClient = apigClientFactory.newClient();
    console.log("apigClient", apigClient);

    try {
        // API GATEWAY
        const getresponse = await apigClient.usernameGet(params, body, additionalParams);
        console.log ("RESPONSE", getresponse.data);

        let profileDetails = getresponse.data;

        if(profileDetails.length === 0 ){
             var div2 = document.createElement("div");
             div2.setAttribute("class","recipe-card");
             document.getElementById("recipe-rows").appendChild(div2);

              var h1 = document.createElement('h1');
              div2.appendChild(h1);
              h1.innerHTML = "Yet to upload yummy recipes.";
              return;
        }

        console.log ("No of recipes", profileDetails.length);
            // Render details
            for (i=0; i < profileDetails.length; i++){
                let profileRecipe= profileDetails[i];
                console.log ("RECIPE DETAILS", profileRecipe);
               // alert(document.getElementById("recipe_count").innerHTML);
               // document.getElementById("recipe_count").innerHTML = profileRecipe.recipe_count;

                var div2 = document.createElement("div");
                div2.setAttribute("class","recipe-card");
                document.getElementById("recipe-rows").appendChild(div2);

                var fig = document.createElement("FIGURE");
                div2.appendChild(fig);
                var img = document.createElement("img");
                img.src = profileRecipe.image;
                fig.appendChild(img);
                //fig.setAttribute("onclick","alert('blah');");
                fig.setAttribute("onclick","loadRecipe('" + profileRecipe.id  + "');");

                // add barter button
                var div3 = document.createElement('div');
                div3.setAttribute('class','card-meta');
                div2.appendChild(div3);

                var p = document.createElement('p');
                p.setAttribute("class","dish-type");
                p.innerHTML = "Barter";
                div3.appendChild(p);
                div3.setAttribute("onclick","loadForm('" + profileRecipe.id  + "');");

                //add recipe title
                var h1 = document.createElement('h1');
                div2.appendChild(h1);
                h1.innerHTML = profileRecipe.title;

            }

    } catch (error){
        console.log("Error", error);
    }
}


async function favRecipeAPI(params, body, additionalParams){

    // Connect to API Gateway
    let apigClient = apigClientFactory.newClient();
    console.log("apigClient", apigClient);

    // Add Favorite Recipes

    try {
        // API GATEWAY
        const getresponse = await apigClient.userfavGet(params, body, additionalParams);
        console.log ("RESPONSE Fav", getresponse.data);

        let profileDetails = getresponse.data;

        if(profileDetails.length === 0 ){
             var div2 = document.createElement("div");
             div2.setAttribute("class","recipe-card");
             document.getElementById("fav-recipe-rows").appendChild(div2);

              var h1 = document.createElement('h1');
              div2.appendChild(h1);
              h1.innerHTML = "No Favorite Recipes.";
              return;
        }

        console.log ("No of recipes", profileDetails.length);
            // Render details
            for (i=0; i < profileDetails.length; i++){
                let profileRecipe= profileDetails[i];
                console.log ("RECIPE DETAILS", profileRecipe);

                var div2 = document.createElement("div");
                div2.setAttribute("class","recipe-card");
                document.getElementById("fav-recipe-rows").appendChild(div2);

                var fig = document.createElement("FIGURE");
                div2.appendChild(fig);
                var img = document.createElement("img");
                img.src = profileRecipe.image;
                fig.appendChild(img);
                //fig.setAttribute("onclick","alert('blah');");
                fig.setAttribute("onclick","loadRecipe('" + profileRecipe.id  + "');");

                // add barter button
                var div3 = document.createElement('div');
                div3.setAttribute('class','card-meta');
                div2.appendChild(div3);

//                var p = document.createElement('p');
//                p.setAttribute("class","dish-type");
//                p.innerHTML = "Barter";
//                div3.appendChild(p);
//                div3.setAttribute("onclick","loadForm('" + profileRecipe.id  + "');");

                //add recipe title
                var h1 = document.createElement('h1');
                div2.appendChild(h1);
                h1.innerHTML = profileRecipe.title;

            }

    } catch (error){
        console.log("Error", error);
    }
}
