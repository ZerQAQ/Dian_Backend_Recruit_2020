<template>
	<div id="app">
		<mt-header title="新文章" fixed>
			<router-link to="/home" slot="left">
				<mt-button icon='back'>返回</mt-button>
			</router-link>
		</mt-header>
		<mt-field rows=1 placeholder="在此输入标题" v-model="title"></mt-field>
		<mt-field rows=20 type="textarea" placeholder="在此输入正文" v-model="content"></mt-field>
		<mt-button @click="send" type="primary" size="large" class="bottom-btn">发布文章</mt-button>
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
				title: "",
				content: ""
			}
		},
		methods: {
			send: function () {
				ajax.postArticle({
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
							message: '发布成功！',
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
	}
</script>

<style lang="scss">
</style>