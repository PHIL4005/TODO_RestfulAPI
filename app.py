from flask import Flask, jsonify, abort, request, make_response, url_for
from flasgger import Swagger, swag_from

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime

import sqlalchemy
import datetime


app = Flask(__name__, static_url_path="")
Swagger(app, config={"specs_route": "/apidocs/", "title": 'A RESTful Todo API'}, merge=True)

# sqlite3 settings
Base = declarative_base()
engine = create_engine('sqlite:///data.db', echo=False)
Session = sessionmaker(bind=engine)


# orm object for CRUDs
class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    due_date = Column(DateTime())
    status = Column(String(1), comment="I: in progress, C: completed, D: deleted")


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Please check the input format!'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'TODO not found'}), 404)


# get all todos
@app.route('/todo/tasks', methods=['GET'])
@swag_from('apidocs/get_all_todos.yml')
def get_tasks():
    session = Session()
    all_todos = {}
    for todo in session.query(Todo).all():
        all_todos[todo.id] = package_task(todo)
    session.close()

    return jsonify(all_todos)


# get a todo by id
@app.route('/todo/tasks/<int:todo_id>', methods=['GET'])
@swag_from('apidocs/get_todo.yml')
def get_task(todo_id):
    session = Session()

    qry_result = session.query(Todo).filter(Todo.id == todo_id)
    if qry_result.count() != 1:
        abort(404)

    session.close()
    return jsonify(package_task(qry_result.first()))


# add a todo
@app.route('/todo/tasks', methods=['POST'])
@swag_from('apidocs/create_todo.yml')
def create_task():
    if not request.json or 'name' not in request.json:
        abort(400)

    session = Session()

    new_todo = Todo(
        name=request.json['name'],
        description=request.json.get('description', ""),
        status="I"
    )

    session.add(new_todo)
    session.commit()
    ret = package_task(new_todo)
    session.close()

    return jsonify(ret), 201


# delete a todo (from database) by id
@app.route('/todo/tasks/<int:todo_id>', methods=['DELETE'])
@swag_from('apidocs/delete_todo.yml')
def delete_task(todo_id):
    session = Session()

    qry_result = session.query(Todo).filter(Todo.id == todo_id)

    if qry_result.count() == 0:
        abort(404)

    qry_result.delete()
    session.commit()
    session.close()

    return jsonify({'result': True})


# update a todo
@app.route('/todo/tasks/<int:todo_id>', methods=['PUT'])
@swag_from('apidocs/update_todo.yml')
def update_task(todo_id):
    if not request.json:
        abort(400)
    if 'status' in request.json and request.json['status'] not in ['I', 'D', 'C']:
        abort(400)

    session = Session()
    qry_result = session.query(Todo).filter(Todo.id == todo_id)

    if qry_result.count() == 0:
        abort(404)

    timestamp = datetime.datetime.now()
    name = request.json.get('name') if 'name' in request.json else qry_result.first().name
    description = request.json.get('description') if 'description' in request.json else qry_result.first().description
    status = request.json.get('status') if 'status' in request.json else qry_result.first().status
    due_date = timestamp if status == 'C' else qry_result.first().due_date if status == 'D' else None

    qry_result.update(
        {
            'name': name,
            'description': description,
            'status': status,
            'due_date': due_date
        }
    )
    session.commit()
    ret = package_task(qry_result.first())
    session.close()

    return jsonify(ret)


# filtering. param could be 'name' and/or 'status'
@app.route('/todo/tasks/filter', methods=['POST'])
@swag_from('apidocs/filtering.yml')
def filtering():
    session = Session()

    status = request.json.get('status') if 'status' in request.json else None
    if status and status not in ['I', 'D', 'C']:
        abort(400)

    name = request.json.get('name').upper() if 'name' in request.json else None

    if status and name:
        qry_result = session.query(Todo)\
            .filter(Todo.status == status)\
            .filter(sqlalchemy.func.upper(Todo.name).like('%' + name + '%')).all()
    elif status:
        qry_result = session.query(Todo).filter(Todo.status == status).all()
    else:
        qry_result = session.query(Todo).filter(sqlalchemy.func.upper(Todo.name).like('%' + name + '%')).all()

    session.close()

    filtered_todos = {}
    for todo in qry_result:
        filtered_todos[todo.id] = package_task(todo)

    return jsonify(filtered_todos)


# sort by 'name' and/or 'due_date'
@app.route('/todo/tasks/sort', methods=['POST'])
@swag_from('apidocs/sort.yml')
def sort_by():
    session = Session()

    # bool
    name = request.json.get('name') if 'name' in request.json else None
    due_date = request.json.get('due_date') if 'name' in request.json else None
    # reversed_flag = request.json.get('due_date') if 'name' in request.json else None

    if name and due_date:
        qry_result = session.query(Todo).filter(Todo.due_date != '').order_by(Todo.name, Todo.due_date).all()
    elif name:
        qry_result = session.query(Todo).order_by(Todo.name).all()
    else:
        qry_result = session.query(Todo).filter(Todo.due_date != '').order_by(Todo.due_date).all()

    session.close()

    filtered_todos = []
    for todo in qry_result:
        filtered_todos.append(package_task(todo))


    return jsonify(filtered_todos)


@app.route('/')
def index():
    return "Hello, World!"


def package_task(todo_object: Todo):
    result = {
        "id": todo_object.id,
        "name": todo_object.name,
        "description": todo_object.description,
        "due_date": todo_object.due_date,
        "status": todo_object.status,
        "uri": url_for('get_task', todo_id=todo_object.id, _external=True)
    }

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
