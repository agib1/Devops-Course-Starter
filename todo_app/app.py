from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config
from todo_app.data.trello_items import add_item, get_items, move_item_to_done

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_items())

@app.route('/add', methods=['POST'])
def add():
    add_item(request.form.get('title'))
    return redirect('/')

@app.route('/complete/<todo_id>', methods=['POST'])
def complete(todo_id):
    move_item_to_done(todo_id)
    return redirect('/')
