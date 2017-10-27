from flask import Flask,jsonify,request,json

app = Flask(__name__)
from pymongo import MongoClient

@app.route('/register', methods = ['POST'])
def homepage():
    data = request.data
    dataDict = json.loads(data)=
    client = MongoClient('')=

@app.route('/topic', methods = ['GET'])
def topicReturn():
    data = request.args.get("")
    dataP = request.args.get("")
    client = MongoClient('')
    return "Invalid ID"

    
@app.route('/topic/add', methods = ['PUT'])
def changeTopic():
        datav = request.data
        dataDict = json.loads(datav)
        data = dataDict.get("")
        dataP = dataDict.get("")
        client = MongoClient('')

@app.route('/topic/delete', methods = ['PUT'])
def deleteTopic():
        datav = request.data
        dataDict = json.loads(datav)
        data = dataDict.get("")
        dataP = dataDict.get("")
        client = MongoClient('')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
