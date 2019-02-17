from flask import Flask #importing flask
from flask_restful import Api, Resource, reqparse #importing modules from flask restful

server = Flask(__name__) #Defining the server
api = Api(server) 

users = [ #Representing Database
    { 
        "name": "Jozef",
        "age": 20,
        "occupation": "Time lord"
    },
    {
      "name": "Ieuan",
       "age": 20,
       "occupation": "Screenwriter"  
    },
    {
        "name": "Faisal",
        "age": 22,
        "occupation": "CTO"
    },
    {
        "name": "Matthew",
        "age": 21,
        "occupation": "Philanthropist"
    }
]


class User(Resource):  #Defining a user resource class

    def get(self, name): #A function that will get a user
        for user in users:  #looks through a dictionary of users, if the name matches on in the database then that data is called and an ok message is sent (200)
            if(name == user["name"]):
                return user, 200
        return "User not found", 404 #if no user found, 404 error returned
    
    def post(self, name): #A function that will post a new user
        parser = reqparse.RequestParser() #creating a parser - converts the data to a json file
        parser.add_argument("age") #adding an age arguement
        parser.add_argument("occupation") #adding an occupation arguement
        args = parser.parse_args() #storing the parsed arguements in a variable

        for user in users:   
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400
        # if the name already exists then display an error message

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }

        users.append(user) #adding the users to the user list
        return user, 201 #returns a successful message


    def put(self, name): #A function that will update details of a user or create a new one
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]): #if the user already exists,
                user["age"] = args["age"] #update the age /occupation 
                user["occupation"] = args["occupation"]
                return user, 200 #return the updated user.

        user = { #if not, create a user
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user) #append the new user/updated user into the user list
        return user, 201 #return the user

    def delete(self, name): #A function that will delete a user from the system/database
        global users #specifying users in a global scope
        users = [user for user in users if user ["name"] != name] #Making a new list without the specified name
        return "{} is deleted.".format(name), 200 # return message


api.add_resource(User, "/user/<string:name>")
server.run(debug=True)
