import gevent
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True

clients = {}
consoles = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/console')
def console():
    return render_template('console.html')


@app.route('/consolesocket')
def consolesocket():
    ws = request.environ['wsgi.websocket']
    consoles.append(ws)
    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/clients')
def api():
    ws = request.environ['wsgi.websocket']
    clients.add(ws)
    _id = request.args.get('id')
    clients[_id] = ws
    print "clients: {0}".format(clients)
    while True:
        message = ws.receive()
        if message is None:
            gevent.sleep(0)
        for key, console in enumerate(consoles):
            try:
                console.send(message)
            except:
                print 'client disconnected'
                # clients.remove(client)

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

