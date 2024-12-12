from flask import Flask, render_template, request, redirect, url_for

from todo_app.flask_config import Config
from todo_app.data.mongo_items import add_item, get_items, move_item_to_done
from todo_app.view_model import ViewModel
from todo_app.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix
from loggly.handlers import HTTPSHandler
from logging import Formatter

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_object(Config())

    app.register_blueprint(blueprint, url_prefix="/login")

    app.logger.setLevel(app.config['LOG_LEVEL'])

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    )
    app.logger.addHandler(handler)

    @app.route('/')
    def index():
        if not github.authorized:
            try:
                app.logger.info("Trying OAuth github login...")
                return redirect(url_for("github.login"))
            except:
                app.logger.error('OAuth github login not complete')
        
        item_view_model = ViewModel(get_items())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        if not github.authorized:
            try:
                app.logger.info("Trying OAuth github login...")
                return redirect(url_for("github.login"))
            except:
                app.logger.error('OAuth github login not complete')
        
        try:
            add_item(request.form.get('title'))
            app.logger.info("Item added: %s", request.form.get('title'))
        except:
            app.logger.error("Failed to add item: %s", request.form.get('title'))

        return redirect('/')

    @app.route('/complete/<todo_id>', methods=['POST'])
    def complete(todo_id):
        if not github.authorized:
            try:
                app.logger.info("Trying OAuth github login...")
                return redirect(url_for("github.login"))
            except:
                app.logger.error('OAuth github login not complete')
    
        try:
            move_item_to_done(todo_id)
            app.logger.info("Item moved to done: %s", todo_id)
        except:
            app.logger.error("Failed to move item to done: %s", todo_id)

        return redirect('/')
    
    return app
