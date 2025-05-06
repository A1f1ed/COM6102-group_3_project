<template>
	<view class="my">
		<!-- 背景 -->
		<view class="my-bg" @click="upBackground">
			<image class="bg-picture" :src="info.userBg" mode="widthFix">
			</image>	
		</view>
		<!-- 头像，昵称，自我介绍 -->
		<view class="my-container">
			<view class="contain-introduce">
				<!-- 头像 -->
				<view class="introduce-left" v-if="isLogin" @click="upAvatar">
					<image class="left-touxiang" :src="info.userImg" mode="widthFix"></image>
				</view>
				<!-- 昵称 自我介绍-->
				<view class="introduce-right"v-if="isLogin">
					<view class="right-nickname">{{info.nickName}}</view>
					<view class="right-desc">这一杯谁不爱! 专业咖啡新鲜式</view>
				</view>
				<!-- 假如用户没有登录，需先登录 -->
				<view class="introduce-isLogin" v-if="!isLogin" @click="goToLogin">
					<text class="introduce-isLogin-text">登录</text>
				</view>
				<!-- 使用v-if指令 -->
			</view>
		</view>
		<!-- 3个人资料 订单 收藏地址 地址管理页面  -->
		<view class="container-info">
			<view class="info-list">
				<view class="list-ziliao">个人资料</view>
				<image class="list-icon" src="../../static/dayufuhao.png" mode="widthFix"></image>
			</view>
			<view class="info-list">
				<view class="list-dingdan">我的订单</view>
				<image class="list-icon" src="../../static/dayufuhao.png" mode="widthFix"></image>
			</view>
			<view class="info-list">
				<view class="list-shoucang" @click="goToCustomerService">校园客服</view>
				<image class="list-icon" src="../../static/dayufuhao.png" mode="widthFix"></image>
			</view>
			<view class="info-list">
				<view class="list-dizhi">地址管理</view>
				<image class="list-icon" src="../../static/dayufuhao.png" mode="widthFix"></image>
			</view>
			<view class="info-list">
				<view class="list-dizhi"  @click="isLogout">退出登录</view>
				<image class="list-icon" src="../../static/dayufuhao.png" mode="widthFix" ></image>
			</view>
		</view>
	</view>
	
</template>

<script>
	//引入图片转换base64的相关脚本
	import{
		pathToBase64,
		baseToPath
	}from'../../js_sdk/mmmm-image-tools/index.js'
	
	export default {
		data() {
			return {
				// 设置一个属性 假设用户没有登陆过false 登陆过true
				isLogin:false,
				info:{},//定义一个属性 存储用户信息
				pic:{}
			}
		},
		onShow() {
			//调用方法1 更改用户登录状态
			this.isGoToLogin();
			this.getUserInfo();
		},
		// created() {
		// 	this.getPic();
		// },
		methods: {
			    goToCustomerService() {
			        uni.navigateTo({
			            url: '/pages/school-customer-service/school-customer-service'
			        })
			    },
			//判断用户是否需要登录
			isGoToLogin(){
				//定义方法1 先获取本地存储的token
				//JSON.stringify方法 表示将某个对象转成json字符串模式
				let token = JSON.parse(localStorage.getItem("token"));
				// console.log("获取本地缓存的token值==>",token);
				
				if(token){
					// 更改islogin布尔值
					this.isLogin = true; //修改为登录状态
				}else{
					this.isLogin = false; //还是未登录状态
				}
			},
			//方法2 点击未登录按钮 跳转到登录页面【非tabbar页面】
			goToLogin(){
				uni.navigateTo({
					url:"/pages/login/login"
				})
			},
			//3 获取用户个人信息
			// 原来
			getUserInfo(){
				if(!this.isLogin){
					return;
				}
				//先获取登录页面本地存储的token
				let tokenString = JSON.parse(localStorage.getItem("token"));
				this.$uni({
					url:"/findMy",
					data:{
						tokenString
					}
				}).then(res => {
					// console.log("getUserInfo() =>",res);
					// console.log("getUserInfo() 注册的用户昵称=>",res[0].nickName);
					// console.log("getUserInfo() 默认的背景图像=>",res[0].userBg);
					// console.log("getUserInfo() 默认的用户头像=>",res[0].userImg);
					//给data（）下的info赋值
					this.info = res[0];
				})
			},
			// 尝试
			// getUserInfo(){
			// 	if(!this.isLogin){
			// 		return;
			// 	}
			// 	//先获取缓存的注册信息中的昵称
			// 	let regInfo = JSON.parse(localStorage.getItem("registerInfo"));
			// 	this.info.nickName = regInfo.nickName;
			// 	// let tokenString = JSON.parse(localStorage.getItem("token"));
			// 	uni.request({
			// 		method:"GET",
			// 		url:"https://mock.mengxuegu.com/mock/640097fd7c016026ff2b9468/mypic",					
			// 		data:{
			// 			appkey:"U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
			// 			nickName:this.info.nickName,
			// 		},
			// 		success:(res) => {
			// 			console.log("尝试getUserInfo: =>",res);
			// 		}
			// 	})
				
			// },
			// 拿默认背景图片和默认头像图片
			getPic(){
				uni.request({
					url:" https://mock.mengxuegu.com/mock/640097fd7c016026ff2b9468/mypic",
					method:"POST",
					data:{
						appkey:"U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
					},
					success:(res) => {
						// console.log("getPic=>",res);
						// console.log("默认的背景图像=>",res.data.picture[1].userBg);
						// console.log("默认的用户头像=>",res.data.picture[0].userAvatar);
						this.pic.userBg = res.data.picture[1].userBg;
						this.pic.userImg = res.data.picture[0].userAvatar;
					}
				})
			},
			//4 先选择图片作为用户头像 把该选择的头像图片先转成base64图片
			upAvatar(){
				uni.chooseImage({
	
					success:(res) => {
						// console.log("方法4 执行成功的回调函数=>",res);
						// console.log(res.tempFilePaths[0]);
						pathToBase64(res.tempFilePaths[0]).then(base64 => {
							let serverBase64 = base64.replace(/^data:image\/[A-Za-z]+;base64,/, '') 
							
							// console.log("4-先选择图片作为用户头像 serverBase64 =>",serverBase64);
							
							//在方法4中调用方法5 把实参传入方法5中
							this.userImg(serverBase64);
						})
					}
				})
			},
			//方法5 上传已经是base64的用户头像
			userImg(serverBase64Img){
				//
				uni.showLoading({
					title:"用户头像加载中"
					
				})
				//先获取本地存储token
				let tokenString = JSON.parse(localStorage.getItem("token"));
				
				//发起网络请求
				this.$uni({
					url:"/updateAvatar",
					method:"POST",
					data:{
						imgType:"",
						tokenString,
						serverBase64Img
					},//post请求，要设置请求头
					header:{
						'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
					}
					
				}).then(res => {
					// console.log("res =>",res);
					//取消用户头像上传成功加载提示
					uni.hideLoading();
					//调用方法3 获取用户个人信息
					this.getUserInfo();
				})
			},
			// 方法6 先选择图片作为背景 把该选择的背景图片先转成base64图片
			upBackground(){
				uni.chooseImage({
				
					success:(res) => {
						// console.log("方法6  执行成功的回调函数=>",res);
						// console.log(res.tempFilePaths[0]);
						pathToBase64(res.tempFilePaths[0]).then(base64 => {
							let serverBase64Background = base64.replace(/^data:image\/[A-Za-z]+;base64,/, '') 
							
							// console.log("6-先选择图片作为背景 serverBase64Background =>",serverBase64Background);
							
							//在方法6中调用方法7 把实参传入方法7中
							this.userBackgroundImg(serverBase64Background);
						})
					}
				})
			},
			
			// 方法7 上传已经是base64的背景图片
			userBackgroundImg(serverBase64Img){
				//
				uni.showLoading({
					title:"背景图片加载中"
					
				})
				//先获取本地存储token
				let tokenString = JSON.parse(localStorage.getItem("token"));
				
				//发起网络请求
				this.$uni({
					url:"/updateUserBg",
					method:"POST",
					data:{
						imgType:"",
						tokenString,
						serverBase64Img
					},//post请求，要设置请求头
					header:{
						'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
					}
					
				}).then(res => {
					console.log("res =>",res);
					//取消用户头像上传成功加载提示
					uni.hideLoading();
					//调用方法3 获取用户个人信息
					this.getUserInfo();
				})
			},
			// isLogout(){
			// 	let token = JSON.parse(localStorage.getItem("token"));
			// 	// console.log("获取本地缓存的token值==>",token);
				
			// 	if(token){
			// 		// 更改islogin布尔值
			// 		this.isLogin = false; //修改为登录状态
			// 	}else{
			// 		this.isLogin = true; //还是未登录状态
			// 	}
			// }
			isLogout(){
				// let that=this
				// console.log(111);
				uni.showModal({
					title:'提示',
					content:'是否退出登录',
					confirmColor:"#0c34ba",
					success:(res) => {
						if(res.confirm){
							// console.log("确定-退出登录");
							uni.setStorageSync("token","")
							// that.loginIs()
							this.isLogin = false;
							
						}else if(res.cancel){
							// console.log('取消-退出登录');
						}
					}
				})
				// let token = JSON.parse(localStorage.getItem("token"));
				// 	// console.log("获取本地缓存的token值==>",token);
					
				// 	if(token){
				// 		// 更改islogin布尔值
				// 		this.isLogin = false; //修改为登录状态
				// 	}else{
				// 		this.isLogin = true; //还是未登录状态
				// 	}
				}
			}
			
		}
	// }
</script>

<style>
	.my{
		height: calc(100vh - 100rpx);
		background-color: #efeff0;
	}
	.my-container{
		display: flex;
		justify-content: center;
	}
	.contain-introduce{
		position: relative;
		top: -100rpx;
		display: flex;
		width: 85%;
		padding: 20rpx;
		background-color: rgba(237, 236, 236, 0.8);
		border-radius: 25rpx 25rpx 0 0;
	}
	.bg-picture{
		width: 100%;
	}
	.introduce-left{
		width: 160rpx;
		height: 160rpx;
		border-radius: 50%;
		overflow: hidden;
		border: 20rpx solid #fff;
		margin-right: 30rpx;
	}
	.left-touxiang{
		width: 100%;
		height: 100%;
	}
	.introduce-right{
		position: absolute;
		left: 240rpx;
		width: calc(100% - 240rpx);
	}
	.right-nickname{
		padding: 20rpx 0;
		font-weight: bold;
		color: #0000ff;
		font-weight: bold;
	}
	.right-desc{
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		font-size: 26rpx;
		color: #545454;
		/* font-weight: bold; */
	}
	.container-info{
		position: relative;
		top: -100rpx;
		margin: 0 36rpx;
		padding: 0 20rpx;
		background: #fff;
		border-radius: 25px;
	}
	.info-list{
		display: flex;
		justify-content: space-between;
		align-items: center;
		height: 100rpx;
		border-bottom: 1rpx solid #ddd;
		font-size: 28rpx;
		color: #666;
	}
	.info-list:last-child{
		border-color: #fff;
	}
	.list-icon{
		width: 28rpx;
	}
	.introduce-isLogin {
		background-color: #9cbee7;
		padding: 30rpx 50rpx;
		border-radius: 5px;
		width: 338.75px;
	}
	.introduce-isLogin-text{
		padding-left: 110px;
		font-weight: bold;
		font-size: 18px;
		letter-spacing: 1.55px;
	}
</style>
