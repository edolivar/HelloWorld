from flask import Flask
from flask import request
from flask import jsonify
import json
from flask_cors import CORS
import uuid
from model_mongodb import User

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

users = {
   'users_list' : [ ]
}

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      subdict = {'users_list' : []}
      if search_username or search_job:
         if search_username :
            for user in users['users_list']:
               if user['name'] == search_username:
                  subdict['users_list'].append(user)
         if search_job :
            for user in users['users_list']:
               if user['job'] == search_job:
                  subdict['users_list'].append(user)
         return subdict
      users = User.find_all()
      return {"user_list" : users}
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd['id'] = str(uuid.uuid1())
      users['users_list'].append(userToAdd)
      resp = jsonify(userToAdd)
      resp.status_code = 201
      return resp
   elif request.method == 'DELETE':
      userToDelete = request.get_json()
      users['users_list'].remove(userToDelete)
      resp = jsonify(success=True)
      resp.status_code = 204
      return resp

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
   if request.method == 'GET':
      if id :
         for user in users['users_list']:
            if user['id'] == id:
               return user
         return ({})
      return users

