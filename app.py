from flask import Flask, render_template, request
import main_code
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

client = MongoClient('mongodb+srv://lakshay:lakshaygargd@form.lsyxxi0.mongodb.net/')
db = client['twitter']
collection = db["trending_data"]

def insert_in_mongo(L):
    doc = {"IP": L[0]}
    for i in range(1, len(L)):
        doc[f'Trend {i}'] = L[i]
    
    # Insert the document into the collection
    insert_result = collection.insert_one(doc)
    
    # Retrieve the inserted document by its _id
    mongo_data = collection.find_one({"_id": insert_result.inserted_id})
    
    return mongo_data
    #print(f"Document inserted with _id: {insert_result.inserted_id}")

def retrieve_from_mongo():
    return(collection.find().sort("timestamp", -1).limit(1))
    
app = Flask(__name__)

def refine(L):
    for i in range(len(L)):
        L[i] = L[i].replace("\n", ' - ')
        L[i] = L[i].replace(" · Trending", "")
    return L

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/routename', methods=['POST'])
def process_form():
    trending_topics = refine(main_code.trending_topics())
    topics = []
    for i in range(1,len(trending_topics)):
        topics.append(f"Topic : {i}")
        topics.append(trending_topics[i])
    topics.append(f"IP : {trending_topics[0]}")
    
    mongoData = insert_in_mongo(trending_topics)
    
    return render_template('index2.html', topics=topics , mongo_data = mongoData)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=4000, debug=True)

