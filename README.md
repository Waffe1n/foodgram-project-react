 # Foodgram 
```
username: admin
password: admin
```

## About 

**Foodgram** is your loayal grocery assistant app, helping you to choose a tasty recipes for all your planned meals, get their components in a short convenient PDF-list to take with you in a grocery store. Track new recipes of your favorite chefs, add them to favorite short-list not to lose them.

### Technoligoies

 - **Python** 3.7.9
 - **Django** 3.2.16 with **DRF** 3.12.4
 -  Web-server provided by **Nginx** 
 - DB powered by PostgreSQL

### Features

- Choose from many recipes, filtering them by supposed meal time tag.
- Create your own recipes — we have **more than 2.000** prepared ingredients to easily add them to your recipe's ingredient list. Don't forget to add a nice picture of your course!
- View user profiles to check all their recipes. Subscribe to their updates to stay tuned!
- Add recipes to your shopping cart and print nicely composed ingredient list, counting all the measures for your chosen dishes.
- Token-based authentication is implemented - don't lose all your favorite recipes!

## Run project inside docker container
1. Install docker, docker-compose on your machine. Copy required files to VM.
```
scp docker-compose.yml <login>@<IP>:/home/<login>/infra/docker-compose.yml
scp nginx.conf <login>@<IP>:/home/<login>/infra/nginx.conf
scp .env <login>@<IP>:/home/<login>/infra/.env
```
2. Login to you VM and run the compose file
```
cd infra/
sudo docker-compose -f docker-compose.yml up -d
```

3. Make migrations and collect static
```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic
```

4. Load database with ingredient, tag data, and some testing recipes
```
sudo docker-compose exec backend python manage.py loaddata dump.json
```

## API endopints description 

-   `/api/users/`  **GET** returns list of users. **POST** to register new user. Available to anyone.
    
-   `/api/users/{id}`  **GET** returns user by ID.  Available to anyone.
    
-   `/api/users/me/`  **GET** returns current active user.  Available to authorized users.
    
-   `/api/users/set_password`  **POST**  request to change password. Available to authorized users.
    
-   `/api/auth/token/login/`  **POST** request to get authorization token (log in). 
    
-   `/api/auth/token/logout/`  **POST** request to delete authorization token (log out). 
    
-   `/api/tags/`  **GET** request to get list of tags. Available to anyone.
    
-   `/api/tags/{id}`  **GET** request to get tag info by it's id. Available to anyone.
    
-   `/api/ingredients/`  **GET** request to get ingredients list info. Filtered by first letters in request. Available to anyone.
    
-   `/api/ingredients/{id}/`  **GET** request shows info of exact ingredient by its id.
    
-   `/api/recipes/`  **GET** request  shows all recipe list. Search by tag and author is included. Available to anyone. Filtration by query parameter `?is_favorited=1` or `is_in_shopping_cart=1` available for authorized users. **POST** request adds a new recipe. Available to authorized users. 
   
    
-   `/api/recipes/{id}/`  **GET** request shows recipe info by it's id. Available to anyone. **PATCH** request to modify your recipe. Available for object's author. **DELETE** request to delete your recipe. Available for object's author.
    
-   `/api/recipes/{id}/favorite/`  **POST** request to add new recipe to favorite recipes list.  **DELETE** request deletes recipe from favorites. Available for authorized users.
    
-   `/api/recipes/{id}/shopping_cart/`  **POST** request adds new recipe to shopping cart list.  **DELETE** request – removes recipe from shopping cart list. Available for authorized users.
    
-   `/api/recipes/download_shopping_cart/`  **GET** request to download PDF-file with shopping cart list. Available to authorized users.
    
-   `/api/users/{id}/subscribe/`  **GET** request to follow user with requested id. **POST** request to unsubscribe from user with requested id. Available for authorized users.
    
-   `/api/users/subscriptions/`  **GET** request shows all subscriptions of current user. Available for authorized users.



