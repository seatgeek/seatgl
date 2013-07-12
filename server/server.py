import gevent
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True

clients = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api')
def api():
    ws = request.environ['wsgi.websocket']
    clients.append(ws)
    print "clients: {0}".format(clients)
    while True:
        message = ws.receive()
        if message is None:
            gevent.sleep(0)
        for key, client in enumerate(clients):
            print "looping: {}".format(key)
            try:
                client.send(message)
            except:
                print 'client disconnected'
                # clients.remove(client)

        gevent.sleep(0.1)

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

