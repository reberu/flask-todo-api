from project.app import app, db
from flask import jsonify, abort, make_response, request, url_for, render_template
from project.app.models import Tasks

API_URI = '/todo/api/v1.0/tasks'


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/tasks', methods=['GET', 'POST'])
def get_tasks():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_task = Tasks(
            title=post_data['title'],
            description=post_data['description'],
            done=False
        )
        db.session.add(new_task)
        db.session.commit()
        response_object['message'] = 'Task added!'
    else:
        tasks = Tasks.query.all()
        output = []
        for task in tasks:
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'done': task.done
            }
            output.append(task_data)
        response_object['tasks'] = output
    # return jsonify({'tasks': list(map(make_public_task, output))})
    return jsonify(response_object)


@app.route(API_URI + '/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    # task = list(filter(lambda t: t['id'] == task_id, tasks))
    if not task:
        abort(404)
    return jsonify({'task': task.as_dict()})


@app.route(API_URI, methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    content = request.json
    new_task = Tasks(
        title=content['title'],
        description=content['description'],
        done=False
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'task': new_task.as_dict()}), 201


@app.route(API_URI + '/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    content = request.json
    if not task:
        abort(404)
    if not content:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    if 'title' in content:
        task.title = content['title']
    if 'description' in content:
        task.description = content['description']
    if 'done' in content:
        task.done = content['done']
    db.session.commit()
    return jsonify({'task': task.as_dict()})


@app.route(API_URI + '/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if not task:
        abort(404)
    del task
    Tasks.query.filter_by(id=task_id).delete()
    db.session.commit()
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
