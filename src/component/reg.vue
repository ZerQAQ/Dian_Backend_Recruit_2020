<template>
	<div id="app">
		<mt-field label="昵称" v-model="nick" placeholder="请输入昵称"></mt-field>
		<mt-field label="帐号" v-model="id" placeholder="请输入ID"> </mt-field>
		<mt-field label="密码" v-model="pwd" type="password" placeholder="请输入密码"></mt-field>
		<mt-cell :title="'当前区域: ' + area">
			<mt-button @click.native="sheetVisible = true"> 选择地区 </mt-button>
		</mt-cell>
		<br>
		<mt-button type="primary" @click.native=reg size="large">注册</mt-button>
		<br>
		<mt-button @click.native=login size="large">登录</mt-button>
		<mt-actionsheet :actions="action" v-model="sheetVisible"></mt-actionsheet>
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
				pwd: "",
				nick: "",
				id: "",
				area: '中国',
				blog_type: "China",
				sheetVisible: false,
				action: [{
					name: '中国',
					method: () => { this.blog_type = 'China'; this.area = '中国' }
				}, {
					name: '美国',
					method: () => { this.blog_type = 'USA'; this.area = '美国' }
				}, {
					name: '日本',
					method: () => { this.blog_type = 'Japan'; this.area = '日本' }
				}
				]
			}
		},
		methods: {
			reg: function () {
				ajax.postUser({
					"nick": this.nick.toString(),
					"id": parseInt(this.id),
					"password": this.pwd.toString()
				}, this.blog_type).then(respond => {
					console.log(respond)
					let retc = respond.body.retc
					if (retc == ajax.IDCONFLICT) {
						MessageBox.alert('此帐号已经被注册！', '提示')
					} else if (retc == ajax.OK) {
						Toast({
							message: '注册成功！',
							position: 'bottom',
							duration: config.msgTime
						});
						setTimeout(() => {
							this.$router.push('/login')
						}, config.redirectTime);
					} else {
						MessageBox.alert('出现未知错误', '提示')
					}
				})
			},
			login: function () {
				this.$router.push('./login')
			}
		},
	}
</script>

<style lang="scss">
	#app {
		width: 95%;
		margin-left: 2.5%;
	}

	.btn {
		display: flex;
		justify-content: space-between;
		margin-left: 25%;
		width: 50%;
	}
</style>