from gevent.wsgi import WSGIServer
from werkzeug.debug import DebuggedApplication
from werkzeug.serving import run_with_reloader
from module import manager, app, api

@manager.command
def runserver(bind='0.0.0.0', port=5000, debug=False):
    app.config['DEBUG'] = debug

    if debug:
        @run_with_reloader
        def run_server():
            WSGIServer((bind, port),  DebuggedApplication(app)).serve_forever()

        run_server()
    else:
        WSGIServer((bind, port), app).serve_forever()


if __name__ == '__main__':
    manager.run()
