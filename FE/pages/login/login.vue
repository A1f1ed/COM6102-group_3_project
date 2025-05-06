<template>
	<view class="login">
		<!-- 1.登录页面标题区域 -->
		<h1 class="login-title">登录页面</h1>
		
		<!-- 2.登录页面表单区域 -->
		<!-- model参数 存放表单数据对象 -->
		<u--form class="login-form" :model="login">
			
			<u-form-item label="账号">
				<u--input  type="text" placeholder="请输入手机号" v-model="login.phone"></u--input>
			</u-form-item>
									
			<u-form-item label="密码">
				<u--input  type="password" placeholder="请输入密码" v-model="login.password"></u--input>	
		    </u-form-item>
		
		</u--form>
		
		<!-- 登录页面登录按钮 -->
		<view class="login-btns">
			<u-button type="primary" text="登录" @click="gotoIndex" ></u-button>
		</view>
		
		<!-- 登录页面注册按钮 -->
		<view class="register-btns">
			<u-button type="primary" text="注册" @click="gotoRegister" ></u-button>				
		</view>
		
		<!-- 图片 -->

	</view>
</template>

<script>
	export default {
		data() {
			return {
				//注册信息
				login: {
					phone: "",//存放注册的账号 
					password: "",//存放注册的密码
					nickName: ""
				}
			}
		},
		
		onLoad() {
			
			// console.log("登录页面测试");
			let regData = JSON.parse(localStorage.getItem("registerInfo"));
			// console.log("获取本地缓存的注册信息 => ",regData);
			
			this.login.phone = regData.phone;
			this.login.password = regData.password;
			this.login.nickName = regData.nickName;
		},
		
		methods: {
			// submit(){
				
			// 	// 手机号码第一位以数字1开头，第二位必须是3-9 \d 第三位表示要设置9个数字
			// 	let logPhone = /^1[3-9]\d{9}$/;
			// 	if (!logPhone.test(this.login.phone) || this.login.phone == ""){
			// 		uni.showToast({
			// 			title:"手机号码格式错误",
			// 			icon:"none"
			// 		})
			// 		return;
			// 	}
					
					
			// 	//密码必须包含数字和字母
			// 	let logPassword = /^(?![^a-zA-Z]+$)(?!\D+$)/;
			// 	if (!logPassword.test(this.login.password) || this.login.password == ""){
			// 		uni.showToast({
			// 			title:"密码格式错误",
			// 			icon:"none"
			// 		})
			// 		return;
			// 	}
			
			// },
			
			//登录成功：跳转至首页
			gotoIndex(){
				uni.request({
					method:'POST',
					url:"http://newcoffee.wwp666.cn:10006/login",
					data:{
						appkey:"U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
						phone:this.login.phone,
						password:this.login.password,
					},
					header:{
						'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
					},	
					success:(res) => {
						// console.log("登录成功：跳转至首页-执行成功的回调函数 => ",res);
						//先拿到token，再进行本次存储，方便后续进行用户信息查询
						// let logToken = res.data.token;
						//console.log("检测信息是否获取到 logToken => ",logToken);
						localStorage.token = JSON.stringify(res.data.token);
						
						
						
						uni.switchTab({
							url:"../../pages/index/index"
						})
					}
				})
				// uni.navigateTo({
				// 	url:"../../pages/index/index"
				// })
			},
						
			//跳转至注册页面
			gotoRegister(){
				uni.navigateTo({
					url:"../../pages/register/register"
				})
			}
			
		}
	}
</script>

<style>
		.login-title{
			display: flex;
			/* 主轴 水平居中 对齐 */
			justify-content: center;
			font-size: 56rpx;
			
			/* s设置内边距 */
			padding: 45px;
			
			font-family: "微软雅黑";
			
			letter-spacing: 1.5px
		}
		
		.login-form{
			display: flex;
			/* 让flex项目换轴 从默认的水平方向变成垂直方向 */
			flex-direction: column;
			/* 主轴交叉轴互成90度 */
			align-items: center;
		}
		
		/deep/.u-form-item{
			width: 86%;
		}
		
		/deep/.u-form-item__body__left__content__label{
			font-weight: bold;
			font-family: "黑体";
			letter-spacing:1.5px;
		}
		
		.u-button{
			width: 50%;
			border-radius: 40px;
			background-color: #0c34ba;
			border: #0c34ba;
			font-family: "微软雅黑";
			font-weight: bold;
		}
		
		.login-btns{
			margin-top: 30px;
		}
		
		.register-btns{
			margin-top: 20px;
		}
		
</style>
