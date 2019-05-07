# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_facts_data = mongo.db.mars_facts_data.find_one()

    # Return template and data
    return render_template("index.html", mars_facts_data=mars_facts_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
 #   mars_facts_data = mongo.db.mars_facts_data
    mars_facts_data = scrape_mars.scrape()
    mongo.db.mars_facts_data.update({}, mars_facts_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)