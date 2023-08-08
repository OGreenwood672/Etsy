from flask import Flask, request
from flask_cors import CORS

import json

from Photo import Photo

app = Flask(__name__)
CORS(app)

#flask --app API run
with open("../DefaultRules.json") as f:
    DefaultRules = json.load(f)

@app.route("/rules")
def GetRules():
    print("get")
    print(request.get_json())

@app.route("/rules", methods=["POST"])
def UpdateRules():
    data = request.get_json()
    
    # if data["client"] not in os.listdir("../clients"):
    #     return json.loads("{'status': 404}")

    # if data["rule"].keys()[0] not in DefaultRules.keys():
    #     return json.loads("{'status': 404}")
    
    # if len(data["rule"].keys()) != 1:
    #     return json.loads("{'status': 405}")
    
    with open(f"../clients/{data['client']}/Rules.json", "r") as f:
        CurrentRules = json.load(f)
        CurrentRules[data["rule"]] = data["value"]
    
    with open(f"../clients/{data['client']}/Rules.json", "w") as f:
        json.dump(CurrentRules, f)

    ClientNumber = 1
    img = Photo(ClientNumber)
    img.UpdateImage()
    
    response = app.response_class(
        status=200,
        mimetype='application/json'
    )

    return response