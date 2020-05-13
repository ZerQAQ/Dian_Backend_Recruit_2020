
# 数据库信息
sql = {
    'host': "localhost",
    'user': 'root',
    'password': '123456',
    'charset': 'utf8mb4'
}

# 开放的IP和端口
host = '127.0.0.1'
port = 8080
# 是否开启flask的debug模式
debug_mod = False
# md5加密的盐 数据库中密码不直接存明文
md5_salt = "salt"
# jwt生命周期，单位秒
jwt_lifetime = 3600
# jwt头部
jwt_header = {
    'alg': "HS256"
}
#不同的国家对应的表名 可拓展
tables = {
    "China": "CN",
    "USA": "USA",
    "Japan": "JP"
}