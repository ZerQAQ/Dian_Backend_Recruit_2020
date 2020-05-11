import flask
import config
import db
import json
import time
import os
import jwt

app = flask.Flask(__name__)

OK = 1
JWT_FAIL = -1
VERIFY_FAIL = -1
NOT_EXIST = -2
SERVER_ERROR = -3
FORMAT_ERROR = -4
ID_CONFLICT = -5
LOGIN_FAIL = -6
jwt_key = os.urandom(256)

DBs = {}

def init_database():
    for (k, v) in config.tables.items():
        DBs[k] = db.DB(v)

#快速生成回应体
def respond(cmd, data = {}):
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
            "msg": "source not exist",
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
    elif cmd == LOGIN_FAIL:
        ret = {
            "retc": -6,
            "msg": "id or password wrong",
            "data": data
        }

    return flask.jsonify(ret)

def make_jwt(id, blog_type):
    payload = {
        'iat': time.time(),
        'exp': time.time() + config.jwt_lifetime,
        #包含id(用户id)和blog_type两个自定义字段
        'id': id,
        'blog_type': blog_type
    }
    return jwt.encode(payload, jwt_key, algorithm = config.jwt_header["alg"])

def parse_jwt(jwt_string):
    try:
        data = jwt.decode(jwt_string, jwt_key)
    except: #jwt验证错误
        return JWT_FAIL

    if data['exp'] < time.time():
        return JWT_FAIL
    else:
        return data

# 如果以后要改成session验证，就直接改这个函数就可以了
def verify(data):
    if 'jwt' not in data:
        return VERIFY_FAIL
    else:
        return parse_jwt(data['jwt'])

@app.route('/api/v1/user', methods=["POST"])
def post_user():
    data = json.loads(flask.request.get_data(as_text=True))
    blog_type = flask.request.args.get("blog_type")
    if blog_type not in config.tables:
        return respond(FORMAT_ERROR)

    retc = DBs[blog_type].insert_user(data)

    # 下面的代码相当于：
    # if retc == db.FORMAT_ERROR:
    #    return respond(FORMAT_ERROR)
    # elif retc == db.ID_CONFLICT:
    #    return respond(ID_CONFLICT)
    # elif retc == db.OK:
    #    return respond(OK)
    # 不过下面的写法比较酷
    # 而且情况比较多的时候比较方便

    return respond(
        {
            db.FORMAT_ERROR: FORMAT_ERROR,
            db.ID_CONFLICT: ID_CONFLICT,
            db.OK: OK
        }[retc]
    )


@app.route('/api/v1/login', methods=["POST"])
def post_login():
    data = json.loads(flask.request.get_data(as_text=True))
    blog_type = flask.request.args.get("blog_type")
    if blog_type not in config.tables:
        return respond(FORMAT_ERROR)

    retc, nick = DBs[blog_type].query_user(data)

    if retc != db.OK:
        return respond(
            {
                db.FORMAT_ERROR: FORMAT_ERROR,
                db.NOT_EXIST: LOGIN_FAIL
            }[retc]
        )
    else:
        return respond(OK, {
            "nick": nick,
            "jwt": make_jwt(data["id"], blog_type)
        })

#这是一个修饰器
#可以发现，无论什么API，我们都要先把消息体拿出来，并且检查一下jwt，得到jwt的payload
#然后把payload里的ID拿出来 并且根据payload里的blog_type选择相应的数据库
#这个过程都放在pre里面做

def pre(func):
    def warpper(*args, **kwargs):
        data = json.loads(flask.request.get_data(as_text=True))

        verification = verify(data)
        if verification == VERIFY_FAIL:
            return respond(JWT_FAIL)

        if verification['blog_type'] not in config.tables:
            return respond(FORMAT_ERROR)

        return func(data, DBs[verification['blog_type']], verification['id'], *args, **kwargs)
    return warpper

# 每一个api函数的前三个参数都是data database uid
# 分别是请求的消息体，根据jwt中的blog_type选择的database，jwt中的id
# 由pre处理后传给函数

@app.route('/api/v1/article', methods=["POST"], endpoint='post_article')
@pre
def post_article(data, database, uid):
    return respond(
       {
           db.FORMAT_ERROR: FORMAT_ERROR,
           db.OK: OK
       }[database.insert_article(data, uid)]
    )

@app.route('/api/v1/article/<aid>', methods=["POST"], endpoint='post_article__aid')
@pre
def post_article__aid(data, database, uid, aid):
    type = flask.request.args.get('type')
    print(type)
    if type not in ['modify', 'delete']:
        return respond(FORMAT_ERROR)

    if type == 'modify':
        return respond(
            {
                db.FORMAT_ERROR: FORMAT_ERROR,
                db.NOT_EXIST: NOT_EXIST,
                db.OK: OK
            }[database.modify_article(data, aid, uid)]
        )
    elif type == 'delete':
        return respond(
            {
                db.NOT_EXIST: NOT_EXIST,
                db.OK: OK
            }[database.delete_article(aid, uid)]
        )

@app.route('/api/v1/article', methods=["GET"], endpoint="get_article")
@pre
def get_article(data, database, uid):
    return respond(OK, (lambda articles: {
        "num": len(articles),
        "articles": articles
    })(database.query_article_by_uid(uid)))

@app.route('/api/v1/article/<aid>', methods=["GET"], endpoint="get_article__aid")
@pre
def get_article(data, database, uid, aid):
    retc, article = database.query_article_by_id(aid, uid)
    if retc != db.OK:
        return respond({
            db.NOT_EXIST: NOT_EXIST
        }[retc])
    else:
        return respond(OK, article)

if __name__ == '__main__':
    init_database()
    app.run(host = "127.0.0.1", port = 8080, debug = config.debug_mod)