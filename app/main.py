from flask import Flask
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

# views
from  app.views.index import index

app = Flask(__name__)

bootstrap = Bootstrap5(app)

# register views
app.register_blueprint(index)

### error handlers ###
def page_not_found(e):
    return render_template('404.html')
app.register_error_handler(404, page_not_found)

def other_errors(e):
    return render_template('other_errors.html', error=e)
[app.register_error_handler(error, other_errors) for error in [400, 403, 410, 500]]


app.config['BOOTSTRAP_SERVE_LOCAL'] = True
