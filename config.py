
# 数据库信息
sql = {
    'host': "localhost",
    'user': 'root',
    'password': '123456',
    'database': 'dian',
    'charset': 'utf8mb4'
}

# md5加密的盐 数据库中密码不直接存明文
md5_salt = "salt"
# 日志输出目录
log_dir = "log"
# 是否自动创建表 （如果数据库中已经有相应的数据库和表的话 就填Flase）
create_table_automatically = False