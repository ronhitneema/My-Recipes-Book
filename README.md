# My Recipes Book

## Dashboard
<img src= "frontend/images/Dashboard.jpeg" width=650>

## Architecture
<img src= "frontend/images/architecture.png" width=650>

## Chatbox
<img src= "frontend/images/chatbox.jpg" width=650>

# My Recipes Book

My Recipes Book is a project that allows users to manage their collection of recipes, search for new recipes, and interact with a chatbot for recipe-related queries. It also includes a recommendation system powered by Amazon Personalize and a barter feature for arranging food exchange meetups.

The My Recipes Book project is a recipe management application that incorporates various features to enhance the user experience. The architecture of the project revolves around enabling users to search for recipes, receive personalized recommendations, interact with a chatbot for assistance, and participate in a food exchange barter.

At the core of the architecture, AWS Lambda functions are utilized to handle different functionalities of the application. These functions are written in Python and are responsible for tasks such as recipe insertion, recipe searching, saving recipes, and searching for recipes by ID. This serverless approach allows for scalability and efficient resource utilization.

The frontend of the application is built using HTML, CSS, and JavaScript, providing an intuitive user interface for seamless recipe browsing and interaction. Users can easily search for recipes using keywords and view detailed information, including ingredients, instructions, and cooking time. They also have the ability to save recipes for future reference.

To enhance the user experience, the application incorporates a chatbot feature. The chatbot utilizes Natural Language Processing (NLP) algorithms to understand user queries and provide relevant responses. It supports both text-based and voice-based interactions, allowing users to ask cooking-related questions, receive recipe recommendations, and seek assistance with their culinary endeavors.

The recommendation system, powered by Amazon Personalize, plays a crucial role in providing personalized recipe suggestions to users. It analyzes user preferences, past interactions, and saved recipes to generate tailored recommendations, enhancing the discovery of new and interesting dishes.

Additionally, the project includes a food exchange barter feature, fostering a sense of community and culinary exploration. Users can arrange meetups to exchange homemade dishes, connecting with other food enthusiasts interested in sharing their culinary creations.

The application leverages Amazon DynamoDB as the database for storing recipe data, user profiles, and other relevant information. This NoSQL database ensures scalability, performance, and flexibility in managing the application's data.

Integration with the Mapbox API enables the inclusion of map-related functionalities within the application. This integration allows users to visualize recipe locations, find nearby food-related establishments, and explore culinary destinations.

Version control for the project is managed using Git, ensuring efficient collaboration and code management among team members.

Overall, the architecture of the My Recipes Book project combines backend AWS Lambda functions, frontend web technologies, NLP algorithms, recommendation systems, a food exchange barter, and database and map integrations to create a comprehensive recipe management application with an intuitive user experience and personalized features.

## Features

- Search for recipes: Users can search for recipes using single or double keyword searches, making it easy to find specific dishes or ingredients.
- View and save recipes: Once a recipe is found, users can view its details, including ingredients, instructions, and cooking time. They also have the option to save recipes for future reference.
- Add custom recipes: Users can add their own custom recipes to the app, allowing them to keep track of their personal favorites and unique creations.
- Chatbot: The chatbot feature enables users to interact with a conversational agent to get recipe recommendations, ask cooking-related questions, or receive assistance with their culinary endeavors. The chatbot supports both text-based and voice-based interactions.
- Recommendation system: Powered by Amazon Personalize, the recommendation system analyzes user preferences and provides personalized recipe suggestions based on their previous interactions and saved recipes.
- Barter: The barter feature allows users to arrange meetups for food exchange. They can connect with other users interested in trading their homemade dishes, fostering a sense of community and culinary exploration.

## Tech Stack
- Backend: AWS Lambda, Python
- Frontend: HTML, CSS, JavaScript
- Database: Amazon DynamoDB
- Chatbot: Natural Language Processing (NLP) algorithms
- Recommendation System: Amazon Personalize
- Map Integration: Mapbox API
- Version Control: Git

## Folder Structure

The project's folder structure is organized as follows:

- `.idea`: Directory containing project-specific configurations and settings.
- `Spoonacular`: Directory with recipe-related functionalities and user profiles.
- `load-recipe-mapbox`: Directory housing Lambda functions created by Bornita, responsible for handling recipe loading and map-related operations.
- `recipe_insert`: Directory for updating the Lambda function responsible for inserting recipes.
- `recipe_search`: Directory for updating the Lambda function responsible for recipe searches.
- `save_recipe`: Directory for updating the Lambda function responsible for saving recipes.
- `search-recipe-ID`: Directory for updating the Lambda function responsible for searching recipes by ID.
- `add_new_recipe2.py`: File containing fixes for search and add recipe Lambda functions.
- `barterNotification.py`: File containing Lambda functions created by Bornita, handling barter-related notifications.
- `load-fav.py`: File for updating the `load-fav` Lambda function.
- `load-profile.py`: File containing Lambda functions created by Bornita, linking user profiles to recipes.
- `load-recipe.py`: File containing Lambda functions created by Bornita, handling recipe loading.
- `personalize.py`: File linking user profiles to the recommendation system.
- `search_for_recipes2.py`: File responsible for searching recipes within the application.

## Getting Started

To run the My Recipes Book project locally, follow these steps:

1. Clone the repository to your local machine.
2. Set up the necessary dependencies and environment variables.
3. Run the project using the preferred development environment or command-line tool.
4. Access the application through the provided URL or local server.

Please refer to the project documentation or specific directories/files for more detailed instructions on configuration and setup.

## License

This project is licensed under the [MIT License](LICENSE.txt).


