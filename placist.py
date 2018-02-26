from gmaps import GMaps, save
from rq import Queue
from rq.job import Job
from worker import conn
from flask import Flask, render_template, request, send_file, jsonify



app = Flask(__name__)
q = Queue(connection=conn)


@app.route('/', methods=['GET'])
def index():
    return render_template('form.html', backend='google')


@app.route('/enqueue', methods=['POST'])
def enqueue():
    scraper = GMaps()
    args = (request.form['term'], request.form['location'], 
                            int(request.form['radius']), int(request.form['points']), 
                            float(request.form['minRating']), float(request.form['maxRating']))
    task = q.enqueue_call(func=scraper.search, args=args, result_ttl=5000, timeout=3600)
    
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
    filename = 'listings.' + task_id + '.csv'
    save(task.result, filename)

    return send_file('listings/' + filename, as_attachment=True)



if __name__=='__main__':
    app.run()
