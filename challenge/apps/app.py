#Imports
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping_images
import scraping
#Set the Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#For the home page route
@app.route("/")
def index():
   mars = mongo.db.mars.facts.find_one()
   mars_images = mongo.db.mars.images.find_one()
   hemispheres = mars_images['hemispheres']
   return render_template("index.html", mars=mars, hemispheres=hemispheres)

@app.route("/scrape_images")
def scrape_images():
   mars = mongo.db.mars.images
   hemispheres = scraping_images.scrape_images()
   mars.update({}, hemispheres, upsert=True)
   return "Scraping Images Successful!"

#Method from the module to get the featured image and facts
@app.route("/scrape_all")
def scrape_all():
   mars = mongo.db.mars.facts
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping All Successful!"

if __name__ == "__main__":
   app.run()
