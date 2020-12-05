import requests
from dotenv import load_dotenv
import os
import logging
from flask import Flask, jsonify, send_from_directory, request
from werkzeug.utils import secure_filename
from feature import describe_image
import json
from flask_cors import CORS
load_dotenv()

databaseId = os.environ.get('ASTRA_CLUSTER_ID')
region = os.environ.get('ASTRA_CLUSTER_REGION')
token = os.environ.get('ASTRA_AUTHORIZATION_TOKEN')

app = Flask(__name__)
CORS(app)

file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

user = ""
score = 0
db_url = "https://{0}-{1}.apps.astra.datastax.com/api/rest/v1/keyspaces/blahaj/tables/sharkhacks/rows/".format(
    databaseId, region)

payload = {"columns": [
    {
        "name": "user",
        "value": user
    }
]}

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "X-Cassandra-Token": token
}


def create_user(user):
    global payload, db_url
    user = user
    score = 0
    response = requests.post(db_url, json=payload, headers=headers).json()
    save_user(user,score)
    if response.get('success') == True:
        return jsonify({'User':user,'Score':score})

def save_user(user,score):
    with open(PROJECT_HOME+'/users.json', "r+") as file:
        data = json.load(file)
        if user not in data.keys():
            data.update({user:score})
        else:
            data[user]=score
        file.seek(0)
        json.dump(data, file)


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


@app.route('/<user>')
def fetch_user(user):
    global db_url
    payload = {"filters": [
        {
            "value": [user],
            "columnName": "user",
            "operator": "eq"
        }
    ]}
    db_url += 'query'
    response = requests.post(db_url, json=payload, headers=headers).json()
    if response.get('count') == 0:
        return create_user(user)
    else:
        with open(PROJECT_HOME+'/users.json', "r+") as file:
            data = json.load(file)
        if user in data.keys():
            return jsonify({'User':user,'Score':data[user]})
        


@app.route('/<user>/upload', methods=['POST'])
def upload_file(user):
    app.logger.info(PROJECT_HOME)
    global score
    global payload
    if request.method == 'POST' and request.files['file']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['file']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        score += describe_image(saved_path)
        if score != 0:
            save_user(user,score)
            return jsonify({"User": user, "Score": score, "Message": "Congrats you have done your part in Captain Blahaj to save the oceans.Captain Blahaj expects your continued Cooperation.Well done"})

        else:
            return jsonify({"User": user, "Score": score, "Message": "Sorry seems like our system couldn't identify your image.Pleas try again later"})

    else:
        return jsonify({"message": "No image found"})

@app.route('/leaderboard')
def leaderboard():
    with open(PROJECT_HOME+'/users.json', "r+") as file:
            data = json.load(file)
            sorted_scores={k: data[k] for k in sorted(data, key=data.get, reverse=True)}   
            return jsonify(sorted_scores)


if __name__ == '__main__':
    app.run(debug=True)
