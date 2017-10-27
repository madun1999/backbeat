from flask import Flask,jsonify,request,json

app = Flask(__name__)
from pymongo import MongoClient

@app.route('/register', methods = ['POST'])
def homepage():
    data = request.data
    dataDict = json.loads(data)
    client = MongoClient('mongodb://kravuri:<backbeat2>@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')

@app.route('/topic', methods = ['GET'])
def bpm():
    data = request.args.get("bpm")
    client = MongoClient('mongodb://kravuri:<backbeat2>@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
    return null

    
@app.route('/topic/add', methods = ['PUT'])
def slowOrFast():
        datav = request.data
        dataDict = json.loads(datav)
        data = dataDict.get("")
        client = MongoClient('mongodb://kravuri:<backbeat2>@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
        return null
    
@app.route('/topic/delete', methods = ['PUT'])
def measureNumbers():
        datav = request.data
        dataDict = json.loads(datav)
        data = dataDict.get("")
        client = MongoClient('mongodb://kravuri:<backbeat2>@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
        return null
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
