<template>
	<div id="app">
		<mt-header fixed title='文章详情'>
			<router-link to="/home" slot="left">
				<mt-button icon='back'>返回</mt-button>
			</router-link>
		</mt-header>
		<h1> {{article.title}} </h1>
		<p class="content"> {{article.content}} </p>
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
				article: {}
			}
		},
		methods: {

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
					this.article = body.data
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
	.content {
		font-size: 1.3em;
		text-align: left;
		word-break: normal;
	}
</style>