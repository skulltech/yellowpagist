from yp import YP, save
from rq import Queue
from rq.job import Job
from worker import conn
from flask import Flask, render_template, request, send_file, jsonify



app = Flask(__name__)
q = Queue(connection=conn)


@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')


@app.route('/enqueue', methods=['POST'])
def enqueue():
    scraper = YP()
    task = q.enqueue_call(func=scraper.search, args=(request.form['term'], request.form['location'], 
                        int(request.form['radius']), float(request.form['minRating']), float(request.form['maxRating'])), 
                        result_ttl=5000, timeout=3600)
    response = {
        'status': 'success',
        'data': {
            'task_id': task.get_id()
        }
    }
    return jsonify(response), 202


@app.route('/tasks/<task_id>', methods=['GET'])
def get_status(task_id):
    task = q.fetch_job(task_id)

    if task:
        response = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
            }
        }
    else:
        response = {'status': 'error'}

    return jsonify(response)


@app.route('/download/<task_id>', methods=['GET'])
def download(task_id):
    task = q.fetch_job(task_id)
    save(task.result)
    return send_file('listings.csv')



if __name__=='__main__':
    app.run()
