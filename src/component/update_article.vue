<template>
	<div id="app">
		<mt-header title="新文章" fixed>
			<router-link to="/home" slot="left">
				<mt-button icon='back'>返回</mt-button>
			</router-link>
		</mt-header>
		<mt-field rows=1 placeholder="在此输入标题" v-model="title"></mt-field>
		<mt-field rows=20 type="textarea" placeholder="在此输入正文" v-model="content"></mt-field>
		<mt-button @click="send" type="primary" size="large" class="bottom-btn">确认修改</mt-button>
	</div>
</template>

<script>
	import { config } from '../script/config.js'
	import { ajax } from '../script/ajax.js'
	import { MessageBox } from 'mint-ui'
	import { Toast } from 'mint-ui';
	export default {
		name: 'app',
		data() {
			return {
				msg: 'Welcome to Your Vue.js App',
				title: "",
				content: ""
			}
		},
		methods: {
			send: function () {
				let id = this.$route.params.id
				ajax.postArticle_Id_Update(id, {
					"title": this.title,
					"content": this.content
				}, this.$parent.jwt).then((respond) => {
					console.log(respond)
					let body = respond.body
					if (body.retc == ajax.JWTFAIL) {
						MessageBox.alert('登录已过期', '提示').then(() => {
							this.$router.push('/login')
						})
					} else if (body.retc == ajax.OK) {
						Toast({
							message: '修改成功！',
							position: 'bottom',
							duration: config.msgTime
						});
						setTimeout(() => {
							this.$router.push('/home')
						}, config.redirectTime);
					} else {
						Toast({
							message: '出现了未知错误',
							position: 'bottom',
							duration: config.msgTime
						});
					}
				})
			}
		},
		beforeMount() {
			let id = this.$route.params.id
			ajax.getArticle_Id(id, this.$parent.jwt).then((respond) => {
				console.log(respond)
				let body = respond.body
				if (body.retc == ajax.JWTFAIL) {
					MessageBox.alert('登录已过期', '提示').then(() => {
						this.$router.push('/login')
					})
				} else if (body.retc == ajax.OK) {
					this.title = body.data.title
					this.content = body.data.content
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
</style>