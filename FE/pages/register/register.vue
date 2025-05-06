<template>
	<view class="register">
		
		<!-- 1.页面标题区域 -->
		<h1 class="register-title">注册</h1>
		
		<!-- 2.页面表单区域 -->
		<!-- model参数 存放表单数据对象 -->
		<u--form class="register-form" :model="register">
			
			<u-form-item label="账号">
				<u--input  type="text" placeholder="请输入手机号" v-model="register.phone"></u--input>
			</u-form-item>
						
			<u-form-item label="昵称">
				<u--input  type="text" placeholder="请输入昵称" v-model="register.nickName"></u--input>
			</u-form-item>
						
			<u-form-item label="密码">
				<u--input  type="password" placeholder="请输入密码" v-model="register.password"></u--input>	
		    </u-form-item>

			<u-form-item label="确认密码">
				<u--input  type="password" placeholder="请确认密码" v-model="register.password_confirm"></u--input>	
		    </u-form-item>

		</u--form>
		
		<view class="u-alert-item">
			<u-alert
			    description="说明:用户名必须为4至16位（可以包含字母、数字、下划线、减号）; 密码必须包含数字和字母"
			    type="primary"
			></u-alert>
		</view>
		
		<!-- 页面注册按钮 -->
		<view class="register-btns">
			<u-button type="primary" text="注册" @click="submit"></u-button>
		</view>
		
		<!-- 底部图片 -->
				



	</view>
</template>

<script>
	export default {
		data() {
			return {
				//注册信息
				register:{
					phone:"",//存放注册的账号 
					nickName:"",//存放注册的昵称
					password:"",//存放注册的密码
					password_confirm:"",//存放确认的密码
					
					// title:'',
					// description:'',
				},
				
				

			}
		},
		
		
		methods: {
			// gotoLogin(){
			// 	uni.navigateTo({
			// 		url:"../../pages/login/login"
			// 	})
			// },
			
			submit(){ 
				
				// 手机号码第一位以数字1开头，第二位必须是3-9 \d 第三位表示要设置9个数字
				let regPhone = /^1[3-9]\d{9}$/;
				if (!regPhone.test(this.register.phone) || this.register.phone == ""){
					uni.showToast({
						title:"手机号码格式错误",
						icon:"none"
					})
					return;
				}
					
					
				// 用户名正则，4到16位（字母，数字，下划线，减号）	
				let regNickName = /^[a-zA-Z0-9_-]{4,16}$/;
				if (!regNickName.test(this.register.nickName) || this.register.nickName == ""){
					uni.showToast({
						title:"昵称格式错误",
						icon:"none"
					})
					return;
				}
				
					
				// 密码必须包含数字和字母	
				let regPassWord = /^(?![^a-zA-Z]+$)(?!\D+$)/;
				if (!regPassWord.test(this.register.password) || this.register.password == ""){
					uni.showToast({
						title:"密码格式错误",
						icon:"none"
					})
					return;
				}
				
				// 确认密码 再次验证
				if (this.register.password_confirm !== this.register.password ){
					uni.showToast({
						title:"第二次输入的密码与第一次不符",
						icon:"none",
					})
					return;
				}
				
				uni.request({
					method:"POST",
					url:"http://newcoffee.wwp666.cn:10006/register",
					data:{
						appkey:"U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
						phone:this.register.phone,
						nickName:this.register.nickName,
						password:this.register.password,						
						password_confirm:this.register.password_confirm,
					},
					header:{
						'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
					},					
					success: (res) => {
						// console.log("收到开发者服务器 成功返回的回调函数=>",res);
						// console.log("检测注册信息是否获取到 this.register=>",this.register)
						localStorage.registerInfo = JSON.stringify(this.register);
					}
				})
				
				// 跳转到登录页面
				uni.navigateTo({
					url:"../../pages/login/login"
				})

			},
			
			
			
		}
	}
</script>
		
<style>
		.register-title{			
			display: flex;
			/* 主轴 水平居中 对齐 */
			justify-content: center;
			font-size: 56rpx;
			
			/* 设置内边距 */
			padding-top: 20px;
			padding-bottom: 20px;
			
			/* 设置字体和字体间间距 */
			font-family: "微软雅黑";
			letter-spacing: 3px
		}
		
		.register-form{
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
			/* 设置表单字体粗细、字体 */
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
		
		.register-btns{
			/* margin-top: 2px; */
			margin-bottom: 25px;
			
		}
		
		.u-alert-item {
			flex: 1;
			/* margin-bottom: 10px; */
			
			
			}
			
		/deep/.u-alert{
			padding: 10px;
			margin-top: 5px;
			margin-bottom:30px ;
			margin-left: 15px;
			margin-right: 15px;
			font-weight:140;
			font-size:12px ;
			text-align: center;
			letter-spacing: 1.55px;
			line-height:19px;
			font-family: "黑体";
			
		}
		.foot-banner{
			
			background-color: #0c34ba;
			display: flex;
			align-items: baseline;
			

		}
		
		.image-bg{
			width: 100%;
			vertical-align: bottom;
		}
	
			

</style>
