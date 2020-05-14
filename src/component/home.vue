<template>
	<div id="app">
		<mt-header fixed :title="'你好! ' + nick">
			<router-link to="/" slot="left">
				<mt-button icon='back'>退出登录</mt-button>
			</router-link>
		</mt-header>
		<mt-cell v-for="elm in articles" :title="elm.title">
			<mt-button size="small" class="article-btn" @click="showDetail(elm.id)">详情</mt-button>
			<mt-button type="primary" size="small" class="article-btn" @click="modifyArticle(elm.id)">修改</mt-button>
			<mt-button type="danger" size="small" @click="deleteArticle(elm.id)">删除</mt-button>
		</mt-cell>
		<mt-button type="primary" size="large" class="bottom-btn" @click="newArticle">发布新文章</mt-button>
	</div>
</template>

<script>
	import { MessageBox } from 'mint-ui'
	import { ajax } from '../script/ajax.js'
	import { Toast } from 'mint-ui';
	import { config } from '../script/config.js'
	export default {
		name: 'app',
		data() {
			return {
				msg: 'Welcome to Your Vue.js App',
				nick: "",
				articles: []
			}
		},
		methods: {
			showDetail: function (id) {
				this.$router.push('/article/' + id.toString())
			},
			newArticle: function () {
				this.$router.push('/new_article')
			},
			modifyArticle: function (id) {
				this.$router.push('/update_article/' + id.toString())
			},
			deleteArticle: function (id) {
				ajax.postArticle_Id_Delete(id, this.$parent.jwt).then((respond) => {
					console.log(respond)
					let body = respond.body
					if (body.retc == ajax.JWTFAIL) {
						MessageBox.alert('登录已过期', '提示').then(() => {
							this.$router.push('/login')
						})
					} else if (body.retc == ajax.OK) {
						Toast({
							message: '删除成功！',
							position: 'bottom',
							duration: config.msgTime
						});
						this.articles = this.articles.filter((item) => { return item.id != id })
					} else {
						Toast({
							message: '发生了未知错误',
							position: 'bottom',
							duration: config.msgTime
						});
					}
				})
			}
		},
		beforeMount() {
			this.nick = this.$parent.nick
			console.log('mount')
			ajax.getArticle(this.$parent.jwt).then((respond) => {
				console.log(respond)
				let body = respond.body
				if (body.retc == ajax.JWTFAIL) {
					MessageBox.alert('登录已过期', '提示').then(() => {
						this.$router.push('/login')
					})
				} else if (body.retc == ajax.OK) {
					this.articles = body.data.articles
				} else {
					Toast({
						message: '发生了未知错误',
						position: 'bottom',
						duration: config.msgTime
					});
				}
			})
		},
	}
</script>

<style lang="scss">
	.bottom-btn {
		position: absolute;
		bottom: 5%;
		left: 5%;
		width: 90%;
	}

	.article-btn {
		margin-right: 5px;
	}
</style>