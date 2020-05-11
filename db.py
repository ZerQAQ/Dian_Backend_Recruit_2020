import pymysql
import config
import hashlib

# 定义要用到的各种sql语句
# 这样如果以后要改数据库结构，修改语句起来比较方便
_insert_user_cmd = "insert into user (id, password, nick) value (%s, %s, %s)"
_query_user_by_id_password_cmd = "select nick from user where id = %s and password = %s"
_query_user_by_id_cmd = "select count(1) from user where id = %s"

_insert_article_cmd = "insert into article (uid, title, content) value (%s, %s, %s)"
_delete_article_cmd = "delete from article where id = %s"
_modify_article_cmd = "update article set title = %s, content = %s where id = %s"

_query_article_by_id_uid_cmd = "select * from article where id = %s and uid = %s"
_query_article_by_uid_cmd = "select id, title from article where uid = %s"

# 定义返回值常量
OK = 0
FORMAT_ERROR = 1
ID_CONFLICT = 2
NOT_EXIST = 3

# 初始化数据库连接
def init():
    global db
    db = pymysql.connect(**config.sql)
    if config.create_table_automatically:
        pass


# md5加密函数
def _md5(data):
    obj = hashlib.md5(config.md5_salt.encode('utf-8'))
    obj.update(data.encode('utf-8'))
    return obj.hexdigest()

#封装pymysql的函数
def _query(cmd, data):
    global db
    cursor = db.cursor()
    cursor.execute(cmd, data)
    cursor.close()
    db.commit()
    return cursor.fetchall()

def _execute(cmd, data):
    global db
    cursor = db.cursor()
    cursor.execute(cmd, data)
    cursor.close()
    db.commit()

#下面是给server用的接口
def insert_user(user):
    if 'id' not in user or 'password' not in user or 'nick' not in user:
        return FORMAT_ERROR #检查格式是否错误
    elif _query(_query_user_by_id_cmd, (user["id"]))[0][0] == 1:
        return ID_CONFLICT #检查主键是否冲突
    else:
        _execute(_insert_user_cmd, (user['id'], _md5(user['password']), user['nick']))
        return OK

def query_user(user):
    if 'id' not in user or 'password' not in user:
        return FORMAT_ERROR
    else:
        query_result = _query(_query_user_by_id_password_cmd, (user["id"], _md5(user["password"])))
        if len(query_result) == 0:
            return NOT_EXIST #用户不存在
        else:
            return query_result[0][0] #如果存在 返回用户名

def insert_article(article, uid):
    if 'title' not in article or 'content' not in article:
        return FORMAT_ERROR
    else:
        #执行插入语句
        _execute(_insert_article_cmd, (uid, article["title"], article["content"]))
        return OK

def delete_article(id, uid):
    if query_article_by_id(id, uid) == NOT_EXIST:
        return NOT_EXIST
    else:
        _execute(_delete_article_cmd, tuple([id]))
        return OK

def modify_article(article, uid):
    if "id" not in article or "title" not in article or "content" not in article:
        return FORMAT_ERROR
    elif query_article_by_id(article["id"], uid) == NOT_EXIST:
        return NOT_EXIST
    else:
        _execute(_modify_article_cmd, (article["title"], article["content"], article["id"]))
        return OK

def query_article_by_id(id, uid):
    query_result = _query(_query_article_by_id_uid_cmd, (id, uid))
    if len(query_result) == 0:
        return NOT_EXIST
    else:
        return query_result[0]

def query_article_by_uid(uid):
    return _query(_query_article_by_uid_cmd, uid)