import flask
import config
import db
import json

app = flask.Flask(__name__)

OK = 1
JWT_FAIL = -1
NOT_EXIST = -2
SERVER_ERROR = -3
FORMAT_ERROR = -4
ID_CONFLICT = -5

def respond(cmd, data = {}):
    # py居然没有case
    ret = {}
    if cmd == OK:
        ret = {
            "retc": 1,
            "msg": "ok",
            "data": data
        }
    elif cmd == JWT_FAIL:
        ret = {
            "retc": -1,
            "msg": "jwt fail",
            "data": data
        }
    elif cmd == NOT_EXIST:
        ret = {
            "retc": -2,
            "msg": "source not esixt",
            "data": data
        }
    elif cmd == SERVER_ERROR:
        ret = {
            "retc": -3,
            "msg": "server error",
            "data": data
        }
    elif cmd == FORMAT_ERROR:
        ret = {
            "retc": -4,
            "msg": "format error",
            "data": data
        }
    elif cmd == ID_CONFLICT:
        ret = {
            "retc": -5,
            "msg": "id has already esixt",
            "data": data
        }
    return flask.jsonify(ret)

@app.route('/api/v1/user', methods=["POST"])
def post_user():
    data = json.loads(flask.request.get_data(as_text=True))
    retc = db.insert_user(data)
    if retc == db.FORMAT_ERROR:
        return respond(FORMAT_ERROR)
    elif retc == db.ID_CONFLICT:
        return respond(ID_CONFLICT)
    elif retc == db.OK:
        return respond(OK)


if __name__ == '__main__':
    db.init()
    app.run(host = "0.0.0.0", port = 8080, debug = True)