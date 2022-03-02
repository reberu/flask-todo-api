from project.app import app, db
from flask import jsonify, abort, make_response, request, url_for, render_template
from project.app.models import Tasks
from uuid import uuid4

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
            id=uuid4().hex,
            title=post_data.get('title'),
            description=post_data.get('description'),
            done=post_data.get('done')
        )
        db.session.add(new_task)
        db.session.commit()
        response_object['message'] = 'Task added!'
        print(post_data)
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
    return jsonify(response_object)


@app.route('/tasks/<task_id>', methods=['PUT', 'DELETE'])
def single_task(task_id):
    response_object = {'status': 'success'}
    task = Tasks.query.filter_by(id=task_id).first()
    if request.method == 'PUT':
        post_data = request.get_json()
        title = post_data.get('title')
        description = post_data.get('description')
        done = post_data.get('done')
        if title:
            task.title = title
        if description:
            task.description = description
        if done is not None:
            task.done = done
        db.session.commit()
        response_object['message'] = 'Task updated!'
    if request.method == 'DELETE':
        if not task:
            abort(404)
        Tasks.query.filter_by(id=task_id).delete()
        db.session.commit()
        response_object['message'] = 'Task removed!'
    return jsonify(response_object)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
