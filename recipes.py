from flask import Flask, request
from utils import flatten

def add_recipe(db, recipe):
    """if set(recipe.keys()) != {'name', 'email', 'psswd', 'class'}:
        return {"message": "Name, email and password are mandatory."}, 400"""
    
    if db.recipes.find_one(filter={"receita": recipe['receita']}):
        return {"message": "Recipe with this name already exists."}, 409
    
    try:
        db.recipes.insert_one(recipe)
    except:
        return {"message": "Invalid data."}, 400

    return {"message": "recipe added successfully."}, 201


def find_recipe(db, email = None):
    if email is None:
        recipes = db.recipes.find({}, {'_id': 0})
        return {'message': 'recipes found successfully.', 'recipes': list(recipes)}, 200
    recipe = db.recipes.find_one({'email': email}, {'_id': 0})
    if recipe is None:
        return {'message': f'{email} not found.'}, 404
    return {'message': f'{email} was found successfully.', 'recipe': recipe}, 200


def edit_recipe(db, email, recipe):
    code = find_recipe(db, email)['status_code']
    if code != 200:
        return {"message":'recipe not found.'}, 404
    try:
        db.recipes.update_one({'email': email}, {'$set': recipe})
    except:
        return {"message":'Error while trying to update recipe information.'}, 500
    return {"message":'recipe updated successfully.'}, 200

def find_categorias(db, unique=True):
    try:
        categorias = list(db.recipes.find({}, {'categorias' : 1}))
        if unique:
            return {'message' : 'Recipes found successfully', 'data' : set(flatten(categorias)) if flatten(categorias) == [] else ['']}, 200
        else:
            return {'message' : 'Recipes found successfully', 'data' : categorias}, 200
    except:
        return {'message' : 'Error', 'data' : ''}, 400