## TABLE

```
user:
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id       | bigint      | NO   | PRI | NULL    |       |
| password | varchar(32) | YES  |     | NULL    |       |
| nick     | varchar(16) | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+

article:
+---------+---------------+------+-----+---------+-------+
| Field   | Type          | Null | Key | Default | Extra |
+---------+---------------+------+-----+---------+-------+
| id      | bigint        | NO   | PRI | NULL    |       |
| uid     | bigint        | YES  | MUL | NULL    |       | //与user.id有外键约束
| title   | varchar(256)  | YES  |     | NULL    |       |
| content | varchar(1024) | YES  |     | NULL    |       |
+---------+---------------+------+-----+---------+-------+
```

## API

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

### POST /api/v1/article?tyle=new
上传一篇文章
```
{
	jwt: "header.body.sign",
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

### POST /api/v1/article?type=modify
修改一篇文章
```
{
	jwt: "header.body.sign",
	id: 12,
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

### POST /api/v1/article?type=delete
删除一篇文章
```
{
	jwt: "header.body.sign",
	id: 12
}
```
```
{
	retc: 1,
	msg: "ok",
	data: {}
}
```

### GET /api/v1/article
获取一个用户的所有文章
```
{
	jwt: "header.body.sign"
}
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

### GET /api/v1/article/:id 
获取ID为:id的文章
```
{
	jwt: "header.body.sign"
}
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