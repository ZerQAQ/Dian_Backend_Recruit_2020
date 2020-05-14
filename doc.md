## TABLE

```
user:
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id       | bigint      | NO   | PRI | NULL    |       |
| password | varchar(32) | YES  |     | NULL    |       | //存的是密码的md5 不直接存明文
| nick     | varchar(16) | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+

article:
+---------+---------------+------+-----+---------+-------+
| Field   | Type          | Null | Key | Default | Extra |
+---------+---------------+------+-----+---------+-------+
| id      | bigint        | NO   | PRI | NULL    |       |
| uid     | bigint        | YES  | MUL | NULL    |       | //与user.id有外键约束
| title   | varchar(256)  | YES  |     | NULL    |       |
| content | varchar(1024) | YES  |     | NULL    |       | //其实我更倾向于用文件存文章 不过只写个demo就怎么方便怎么来好了
+---------+---------------+------+-----+---------+-------+
```

## API

### 异常retc:

- -1 jwt fail
- -2 source not exist
- -4 format error
- -5 id conflict ID已经被注册
- -6 帐号或密码错误

### POST /api/v1/login
用户登录
```
{
	id: 123
	password: "pwd"
}
```
```
{
	retc: 1,
	msg: "ok",
	data: {
		jwt: "header.body.sign",
		nick: "pwq"
	}
}
```

### POST /api/v1/user
用户注册
```
{
	id: 123,
	nick: "owo",
	password: "pwd"
}
```
```
{
	retc: 1,
	msg: "ok",
	data: {}
}
```

### POST /api/v1/article?jwt=
上传一篇文章
```
{
	title: "qwq",
	content: "xwx"
}
```
```
{
	retc: 1,
	msg: "ok",
	data: {}
}
```

### POST /api/v1/article:id?type=modify?jwt=
修改一篇文章
```
{
	title: "OvO",
	content: "fox"
}
```
```
{
	retc: 1,
	msg: "ok",
	data: {}
}
```

### POST /api/v1/article:id?type=delete?jwt=
删除一篇文章
```
```
```
{
	retc: 1,
	msg: "ok",
	data: {}
}
```

### GET /api/v1/article?jwt=
获取一个用户的所有文章
其实最好做下分页，例如一次请求返回第1~20篇，下一次请求返回21~30篇
不过先做个简单的好了
```
```
```
{
	retc: 1,
	msg: "ok",
	data: {
		num: 2, //文章数量
		article: [
			{
				id: 1,
				title: "OAO"
			},
			{
				id: 2,
				title: "TvT"
			}
		]
	}
}
```

### GET /api/v1/article/:id?jwt=
获取ID为:id的文章
```
```
```
{
	retc: 1,
	msg: "ok",
	data: {
		id: 23,
		title: "xwx",
		content: "ctx"
	}
}
```