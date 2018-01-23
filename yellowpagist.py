from yp import YP, save
from flask import Flask, render_template, request, send_file



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def scrape_listings():
    if request.method == 'POST':
        scraper = YP()
        listings = yp.search(request.form['term'], request.form['location'], 
                            int(request.form['radius']), float(request.form['minRating']))
        
        save(listings)
        return send_file('listings.csv')
    else:
        return render_template('form.html')


if __name__=='__main__':
    app.run()
