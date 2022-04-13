from flask import render_template, request, Blueprint

core = Blueprint('core', __name__)

@core.route('/')
def index() -> str:

    return render_template('index.html', )

@core.route('/info')
def info() -> str:
    return render_template('info.html')
