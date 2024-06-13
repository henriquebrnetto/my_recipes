from flask import Flask, request
from auth import hash_password
from utils import decorate

def add_user(db, user):
    recovery_code = 0
    if set(user.keys()) != {'name', 'email', 'psswd', 'class'}:
        return {"message": "Name, email and password are mandatory."}, 400
    
    if db.users.find_one(filter={"email": user['email']}):
        return {"message": "User with this e-mail already exists."}, 409
    
    hashdec_password = hash_password(decorate(user['psswd']))
    
    user["psswd"] = hashdec_password
    user["recovery_code"] = recovery_code

    try:
        db.users.insert_one(user)
    except:
        return {"message": "Invalid data."}, 400

    return {"message": "User added successfully."}, 201


def find_user(db, email = None):
    if email is None:
        users = db.users.find({}, {'_id': 0})
        return {'message': 'Users found successfully.', 'users': list(users)}, 200
    user = db.users.find_one({'email': email}, {'_id': 0})
    if user is None:
        return {'message': f'{email} not found.'}, 404
    return {'message': f'{email} was found successfully.', 'user': user}, 200


def edit_user(db, email, user):
    code = find_user(db, email)['status_code']
    if code != 200:
        return {"message":'User not found.'}, 404
    try:
        db.users.update_one({'email': email}, {'$set': user})
    except:
        return {"message":'Error while trying to update user information.'}, 500
    return {"message":'User updated successfully.'}, 200

def recovery_code(db, email, code):
    db.users.update_one({'email': email}, {"$set": {'recovery_code' : code}})
    return {'message' : 'Information updated successfully.'}, 200


def del_user(db, email):
    filter = {'email': email}
    user = db.users.find_one(filter)

    if user is None:
        return {"message":'User not found.'}, 404
    
    try:
        db.users_deleted.insert_one(user)
        db.users.delete_one(filter)
    except:
        return {"message":'Error while trying to delete user.'}, 400
    return {"message": 'User deleted successfully.'}, 200


def change_password(db, email, new_psswd):
    new_psswd = hash_password(new_psswd)
    filter = {'email': email}
    try:
        db.users.update_one(filter, {"$set":{'senha':new_psswd, 'recovery_code': 0}})
        return {'message': 'Password changed successfully.'}, 200
    except:
        return {'message': 'Error while trying to update password.'}, 400