from yp import YP
from flask import Flask, render_template, request



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def scrape_listings():
    if request.method == 'POST':
        scraper = YP()
        listings = yp.search(request.form['term'], request.form['location'], 
                            int(request.form['radius']), float(request.form['minRating']))

        return render_template('listings.html', listings=listings)
    else:
        return render_template('form.html')


if __name__=='__main__':
    app.run()
