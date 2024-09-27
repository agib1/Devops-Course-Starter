from flask import Flask, render_template, request, redirect, url_for

from todo_app.flask_config import Config
from todo_app.data.mongo_items import add_item, get_items, move_item_to_done
from todo_app.view_model import ViewModel
from todo_app.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_object(Config())

    app.register_blueprint(blueprint, url_prefix="/login")

    @app.route('/')
    def index():
        if not github.authorized:
            return redirect(url_for("github.login"))
        
        item_view_model = ViewModel(get_items())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        if not github.authorized:
            return redirect(url_for("github.login"))
        
        add_item(request.form.get('title'))
        return redirect('/')

    @app.route('/complete/<todo_id>', methods=['POST'])
    def complete(todo_id):
        if not github.authorized:
            return redirect(url_for("github.login"))
    
        move_item_to_done(todo_id)
        return redirect('/')
    
    return app
