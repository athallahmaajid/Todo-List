from flask_restful import Api, reqparse, abort, Resource
from flask import request
from flask import Blueprint
from .models import Note, db

api_key = "e0684197-eb8d-41e3-8346-8cb332fa9805"

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

def abort_if_todo_doesnt_exist(todo):
    if not todo:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


def require_appkey(view_function):
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        #if request.args.get('key') and request.args.get('key') == key:
        if request.args.get('key') and request.args.get('key') == api_key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

# Todo
# shows a single todo item and lets you delete a todo item
class TodoDetail(Resource):

    @require_appkey
    def get(self, note_id):
        todo = Note.query.get(note_id)
        abort_if_todo_doesnt_exist(todo)
        return {'task': todo.task}

    @require_appkey
    def delete(self, note_id):
        todo = Note.query.get(note_id)
        abort_if_todo_doesnt_exist(todo)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    @require_appkey
    def put(self, note_id):
        args = parser.parse_args()
        todo = Note.query.get(note_id)
        abort_if_todo_doesnt_exist(todo)
        todo.task = args['task']
        return {'task':args['task']}, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    @require_appkey
    def get(self):
        todos = Note.query.all()
        res = []
        for todo in todos:
            res.append({f'{todo.id}' : todo.data})
        return res

    @require_appkey
    def post(self):
        args = parser.parse_args()
        new_todo = Note(data=args['task'])
        db.session.add(new_todo)
        db.session.commit()
        return {'task': new_todo.data}, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(TodoDetail, '/todos/<note_id>')
