from flask import Flask, request
from auth import requires_auth, requires_admin, check_admin, check_auth
from url import mongo_url
from users import add_user, find_user
from recipes import add_recipe, find_categorias
import pymongo

app = Flask("recipeRandomizer")
client = pymongo.MongoClient(mongo_url)
db = client['recipeRandomizer']

#--------------------------------- ROUTES ---------------------------------

#--------------------------------- HOME ---------------------------------

@app.route('/', methods=['GET'])
def home():
    return {'message' : 'Welcome :)'}, 200

#--------------------------------- LOGIN ---------------------------------

@app.route('/login', methods=['GET'])
def login():
    ret = None
    auth = request.authorization
    if check_auth(auth.username, auth.password, db):
        ret = "user"
    if check_admin(auth.username, auth.password, db):
        ret = "admin"
    return {'message' : 'User found successfully.', "data" : ret}, 200

#--------------------------------- USERS ---------------------------------

@app.route('/users', methods=['GET'])
#@requires_admin(db)
def get_users():
    return find_user(db)

@app.route('/users', methods=['POST'])
#@requires_admin(db)
def add_users():
    return add_user(db, request.json)

#--------------------------------- RECIPES ---------------------------------

@app.route('/recipes', methods=['GET'])
@requires_admin(db)
def get_recipes():
    return {'message' : 'Welcome :)'}, 200

@app.route('/recipes', methods=['POST'])
@requires_admin(db)
def add_recipes():
    print(request.json)
    return add_recipe(db, request.json)

@app.route('/recipes/categorias', methods=['GET'])
@requires_admin(db)
def get_categorias():
    return find_categorias(db)

if __name__ == '__main__':
    app.run(debug=True)