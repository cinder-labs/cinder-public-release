#####
# cinder.py
# This starts an instance of a cinder assistant and executes user input
# Created by: Carter Richard
# License: GNU GPL v3
###

##### Setup #####

# Native dependencies

# External dependencies
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

# Internal dependencies
from tinder import *

##### API Endpoints #####

class spark(Resource):
    def get(self):

        userMessage = message()
        userMessage.sender = 'user'
        userMessage.content = 'spark'

        response = activeSession.interactionCycle(userMessage, instance)

        responseMessage = {
            'sender' : response.sender.capitalize(),
            'content' : response.content,
            'transaction' : ''
        }

        return [responseMessage], 200

class interact(Resource):
    def post(self):        

        parser = reqparse.RequestParser() 
        parser.add_argument('sender', required=True, location='json')
        parser.add_argument('content', required=True, location='json')
        parser.add_argument('transaction', required=False, location='json')
        args = parser.parse_args()

        userMessage = message()
        userMessage.sender = args['sender']
        userMessage.content = args['content']
        userMessage.transaction = args['transaction']
        userMessage.authenticate()

        if userMessage.auth == True:
            response = activeSession.interactionCycle(userMessage, instance)

            responseMessage = {
                'sender' : response.sender.capitalize(),
                'content' : response.content,
                'transaction': ''
            }
        else:
            responseMessage = {
                'sender' : 'System',
                'content' : 'Interaction is unauthorized. Provide a valid ethereum transaction hash or run host in centralized paradigm.',
                'transaction': ''
            }

        return [responseMessage], 200


##### API Configuration #####
 
app = Flask(__name__)
api = Api(app)
api.add_resource(spark, '/spark')
api.add_resource(interact, '/interact')

##### Runtime Execution #####
if __name__ == '__main__':

    instance = cinder()
    instance.clear()
    instance.spark()
    activeSession = session(instance)
    app.run(host='0.0.0.0', port=8080)