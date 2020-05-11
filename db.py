import pymysql
import config
import hashlib

# 定义要用到的各种sql语句
# 这样如果以后要改数据库结构，修改语句起来比较方便
# 其实也可以用ORM框架 我用过Go的ORM框架也自己用Go写过一个 不过没做要求我就不学新的了（） 先用自己熟练的做
_insert_user_cmd = "insert into user (id, password, nick) value (%s, %s, %s)"
_query_user_by_id_password_cmd = "select nick from user where id = %s and password = %s"
_query_user_by_id_cmd = "select count(1) from user where id = %s"

_insert_article_cmd = "insert into article (uid, title, content) value (%s, %s, %s)"
_delete_article_cmd = "delete from article where id = %s"
_modify_article_cmd = "update article set title = %s, content = %s where id = %s"

_query_article_by_id_uid_cmd = "select id, title, content from article where id = %s and uid = %s"
_query_article_by_uid_cmd = "select id, title from article where uid = %s"

_create_table_user_cmd = '''
                create table if not exists user(
                id bigint primary key auto_increment,
                password varchar(32),
                nick varchar(16)
                )
            '''

_create_table_article_cmd = '''
                create table if not exists article(
                id bigint primary key auto_increment,
                uid bigint,
                title varchar(256),
                content varchar(1024),
                constraint user
                foreign key(uid) references user(id)
                );           
'''

# 定义返回值常量
OK = 0
FORMAT_ERROR = 1
ID_CONFLICT = 2
NOT_EXIST = 3

# 初始化数据库连接

# md5加密函数
def _md5(data):
    obj = hashlib.md5(config.md5_salt.encode('utf-8'))
    obj.update(data.encode('utf-8'))
    return obj.hexdigest()

class DB:
    #传入的是数据库名称
    def __init__(self, name):
        # 初始化数据库 库不存在建库 表不存在建表
        self.db = pymysql.connect(**config.sql)
        self._execute("create database if not exists " + name)

        self.db = pymysql.connect(**config.sql, database = name)
        self._execute(_create_table_user_cmd)
        self._execute(_create_table_article_cmd)

    # 封装pymysql的函数
    def _query(self, cmd, data = ()):
        cursor = self.db.cursor()
        cursor.execute(cmd, data)
        cursor.close()
        self.db.commit()
        return cursor.fetchall()

    def _execute(self, cmd, data = ()):
        cursor = self.db.cursor()
        cursor.execute(cmd, data)
        cursor.close()
        self.db.commit()

    #下面是给server用的接口
    def insert_user(self, user):
        if 'id' not in user or 'password' not in user or 'nick' not in user:
            return FORMAT_ERROR #检查格式是否错误
        elif self._query(_query_user_by_id_cmd, (user["id"]))[0][0] == 1:
            return ID_CONFLICT #检查主键是否冲突
        else:
            self._execute(_insert_user_cmd, (user['id'], _md5(user['password']), user['nick']))
            return OK

    def query_user(self, user):
        if 'id' not in user or 'password' not in user:
            return FORMAT_ERROR, ''
        else:
            query_result = self._query(_query_user_by_id_password_cmd, (user["id"], _md5(user["password"])))
            if len(query_result) == 0:
                return NOT_EXIST, '' #用户不存在
            else:
                return OK, query_result[0][0] #如果存在 返回用户名

    def insert_article(self, article, uid):
        if 'title' not in article or 'content' not in article:
            return FORMAT_ERROR
        else:
            #执行插入语句
            self._execute(_insert_article_cmd, (uid, article["title"], article["content"]))
            return OK

    def delete_article(self, aid, uid):
        if self.query_article_by_id(aid, uid) == NOT_EXIST:
            return NOT_EXIST
        else:
            self._execute(_delete_article_cmd, tuple([aid]))
            return OK

    def modify_article(self, article, aid, uid):
        if "title" not in article or "content" not in article:
            return FORMAT_ERROR
        elif self.query_article_by_id(aid, uid) == NOT_EXIST:
            return NOT_EXIST
        else:
            self._execute(_modify_article_cmd, (article["title"], article["content"], aid))
            return OK

    def query_article_by_id(self, aid, uid):
        query_result = self._query(_query_article_by_id_uid_cmd, (aid, uid))
        if len(query_result) == 0:
            return NOT_EXIST, {}
        else:
            return OK, {"id": query_result[0][0],
                        "title": query_result[0][1],
                        "content": query_result[0][2]}

    def query_article_by_uid(self, uid):
        return [{"id": elm[0], "title": elm[1]} for elm in self._query(_query_article_by_uid_cmd, uid)]