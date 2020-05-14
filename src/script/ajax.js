import Vue from 'vue'

export var ajax = {
	//root: 'http://121.199.42.103/api/v1',
	root: '/api/v1',
	OK: 1,
	IDCONFLICT: -5,
	NOTEXIST: -2,
	JWTFAIL: -1,
	LOGFAIL: -6,
	getTest: function () {
		return Vue.http.get('http://121.199.42.103' + '/test')
	},
	postUser: function(data, blogType) {
		console.log(data)
		return Vue.http.post(
			this.root + '/user?blog_type=' + blogType,
			data,
			{emulateJson: true}
		)
	},
	postLogin: function(data, blogType){
		return Vue.http.post(
			this.root + '/login?blog_type=' + blogType,
			data,
			{emulateJson: true}
		)
	},
	getArticle: function(jwt){
		return Vue.http.get(
			this.root + '/article?jwt=' + jwt
		)
	},
	getArticle_Id: function(id, jwt){
		return Vue.http.get(
			this.root + '/article/' + id.toString() + '?jwt=' + jwt
		)
	},
	postArticle: function(data, jwt){
		return Vue.http.post(
			this.root + '/article' + '?jwt=' + jwt,
			data,
			{emulateJson: true}
		)
	},
	postArticle_Id_Update: function(id, data, jwt){
		return Vue.http.post(
			this.root + '/article/' + id.toString() + '?jwt=' + jwt + '&type=modify',
			data,
			{emulateJson: true}
		)
	},
	postArticle_Id_Delete: function(id, jwt){
		return Vue.http.post(
			this.root + '/article/' + id.toString() + '?jwt=' + jwt + '&type=delete',
		)
	},
}