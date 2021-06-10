from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_mission_db

# Drops collection if available to remove duplicates
db.mars.drop()

# Creates a collection in the database
# db.mars()


@app.route("/")
def index():
    scraper()
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():
    mars = db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
