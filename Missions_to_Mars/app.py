import scrape_mars
from flask import Flask, render_template, redirect, url_for
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)


# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

#Create root route
@app.route('/')
def root():
	
    #Query MongoDB for data
    mars_coll = client.db.mars_coll.find_one()

    #Render
    return render_template('index.html',mars=mars_coll)

#Create scrape route
@app.route('/scrape')
def rscrape():

    #Create collection for data
    mars_coll = client.db.mars_coll

    #Call scrape_mars.py with scrape function
    data = scrape_mars.scrape()

    #Update collection with dictionary
    mars_coll.update({}, data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)