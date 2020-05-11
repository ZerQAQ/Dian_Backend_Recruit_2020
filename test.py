import pymysql
import config

db = pymysql.connect(**config.sql)
c = db.cursor()
c._execute("select nick from user where id = 1 and password = 1")
c.close()
db.commit()
print(tuple([1]))