<template>
	<view class="home">
		<!-- <image class="logo" src="/static/logo.png"></image>
		<view class="text-area">
			<text class="title">{{title}}</text>
		</view> -->
		<!-- <u-button type="primary" text="确定"></u-button> -->
		<view class="nav">
			
			<view class="nav-left">
				<!-- <text class="nav-sayhi">下午好</text> -->
				<text class="nav-sayhi"> {{this.greetings}} </text>
				<text class="nav-name" v-if="isLogin">{{info.nickName}}</text>
				<text class="nav-name" v-if="!isLogin">Lucky</text>
			</view>
			
			<view class="nav-right" >
				<u-search 
					placeholder="输入商品名称" 
					v-model="keyword" 
					:showAction="false" 
					search-icon-color="#0c34ba"
					searchIconSize=26
					maxlength=15
					:disabled="true"
					@click="gotoSearch()"
					>
					
				</u-search>
				
			</view>
		</view>
	
		<view class="swiperImg">
			<u-swiper 
			:list="swiperImg" 
			height="260" 
			indicator  
			indicatorActiveColor="#ffffff"
			indicatorInactiveColor="rgba(255, 255, 255, 0.35)"			
			autoplay circular 
			interval="3000"
			duration="1000"
			
			>
			<!-- imgMode='widthFix' -->
			</u-swiper>
		</view>
		
		<view class="hot-recommend">
			<!-- 标题 -->
			<view class="recommend-title">
				<text class="title-txt">热品推荐</text>
			</view>
			
			<!-- 商品列表 -->
			<view class="recommend-list">
				<view class="list-items" v-for="(item,index) in HotProduct" :key="index" @click="gotoDetails(item.pid)">
					<!-- 商品图片 -->
					<view class="item-picture">
							<image class="picture-show" :src="item.smallImg" mode="widthFix" ></image>
					</view>
					<!-- 商品中英名称 -->
					<view class="items-chinese-name"> {{item.name}} </view>
					<view class="items-english-name"> {{item.enname}} </view>	
					<!-- 价格 -->
					<view class="items-price">
						<text class="coffee-price">¥{{item.price}}</text>
					</view>
				</view>
			</view>
				
		</view>
<view class="customer-service-btn" @click="goToCustomerService">
    <image src="/static/images/kf.png" mode="aspectFit" style="width: 30px; height: 30px;"></image>
</view>
	</view>	

</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello',
				keyword:"",
				//定义属性 存放轮播图的图片路径
				swiperImg:[],
				//定义属性，存放热卖推荐商品数据
				HotProduct:[],
				// 根据当前时间显示问候语
				greetings:"",
				// 显示登录者的账号昵称
				info:{},
				isLogin:false,
			}
		},
		
		onShow() {
			// this.getGreetings();
			this.isGoToLogin();
			this.getUserInfo();
			
			
		},
		onLoad() {
			// this.getUserInfo();
		},
		created() {
			this.getGreetings();
			
			this.getSwiper();
			
			this.getHotProduct();
		},
		
		methods: {
					goToCustomerService() {
						uni.navigateTo({
							url: '/pages/customer-service/customer-service',
							fail: (err) => {
								console.error('跳转失败:', err);
								uni.showToast({
									title: '跳转失败，请重试',
									icon: 'none'
								});
							}
						});
					},
			getGreetings(){
				var date=new Date();
				var hour=date.getHours();
				var h=parseInt(hour);
				if(h>=0&&h<6){
					this.greetings = "凌晨好";
				}else if (h>=6&&h<12){
				    this.greetings = "早上好";
				}else if (h>=12&&h<14){
				    this.greetings = "中午好";
				}else if (h>=14&&h<18){
				    this.greetings =  "下午好";
				}else if (h>=18){
				    this.greetings = "晚上好";
				}
			},
			isGoToLogin(){
				let token = JSON.parse(localStorage.getItem("token"));
				// console.log("isGoToLogin获取的token值：",token);
				if(token){
					this.isLogin = true;
				}else{
					this.isLogin = false;
				}
			},
			getUserInfo(){
				if(!this.isLogin){
					return;
				}
				
				let tokenString = JSON.parse(localStorage.getItem("token"));
				// console.log("getUserInfo拿到tokenString=>",tokenString);
				this.$uni({
					url:"/findMy",
					data: {
						tokenString
					}
				}).then(res => {
					// console.log("getUserInfo()=>",res);
					// console.log("getUserInfo()=>昵称",res[0].nickName);
					this.info = res[0];
				})
			},
			getSwiper(){
				uni.request({
					// url:"http://www.kangliuyong.com:10002/banner",
					url:"https://mock.mengxuegu.com/mock/64008d727c016026ff2b9455/swiper",
					 
					method:"GET",
					data:{
						appkey:"U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
						},
					success:(res) => {
						// console.log("getSwiper ==>",res);
						let getArr = res.data.data;
						getArr.forEach((item) => {
							this.swiperImg.push(item.imgUrl);
							// console.log("this.swiperImg数组依次添加数组元素 => ",this.swiperImg);
						}
						
						)
					}
				})
			},

			getHotProduct(){
				uni.request({
					url:"http://newcoffee.wwp666.cn:10006/typeProducts",
					method:"GET",
					data:{
						appkey:"U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
						key:"isHot",
						value:1
					},
					success:(res) => {
						//console.log("index res => ",res);
						
						if(res.data.code === 500){
							// console.log("getHotProduct() res => ",res);
							// console.log("getHotProduct() res.data.result => ",res.data.result );
						//给data下的HotProduct重新赋值
						this.HotProduct = res.data.result;
						// console.log("data下的HotProduct重新赋值 => ",this.HotProduct);
						}
					}
				})
			},
			
			gotoSearch(){
					setTimeout(()=>{
						uni.navigateTo({
								url:"../../pages/search/search"},1000)
					})
			},
			gotoDetails(id){
				// console.log("data值获取=>:",id);
				uni.navigateTo({
					url:'../../pages/detail/detail?id='+ id
				})
			}
		}
	}
</script>

<style>
	.nav{
		height: 120rpx;
		display: flex;
		justify-content: space-around;
		align-items: center;
		/* border-bottom:1rpx solid #000 ; */
		background-color: #fff;
	}
	
	.nav-left{
		font-size: 30rpx;
		font-weight: bold;
	}
	
	.nav-sayhi{
		/* margin-right: 10px; */
		color: #555557;
		font-family: "黑体";
		margin-right: 5px;
	}
	
	.nav-name{
		color: #0c34ba;
		font-family: "黑体";
	}
	
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	
	/* 固定搜索框 */
	/deep/.uni-input-input{
		position: absolute;
	}
	/deep/.u-search__content{
		    width: 200px;
		
	}
	/deep/.u-search__content__icon {
	    margin-right: 10rpx;  /* 调整图标位置 */
	}
	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
	
	/* 图片区域 */
	
	.swiperImg{
		margin:20rpx
	}
	
	/* 热卖推荐样式1 */
	/* .recommend-title{
		color: white;
		background-color: #0c34ba;
		margin: 8px;
		padding:6px 17px 6px 17px;
		width: 64px;
		border-radius:0px 25px 0px 0px
	} */
	
	/* 热卖推荐列表 */
	.home{
		background-color: #efeff0; //正式颜色
		/* background-color: #aaf7de  //测试颜色 */
			.customer-service-btn {
				position: fixed;
				right: 30rpx;
				bottom: 120rpx; // 距离底部120rpx，避免与tabBar重叠
				width: 100rpx;
				height: 100rpx;
				background-color: #0c34ba;
				border-radius: 50%;
				display: flex;
				justify-content: center;
				align-items: center;
				box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);
				z-index: 999;
				
				// 添加点击效果
				&:active {
					transform: scale(0.95);
					opacity: 0.9;
				}
				
				// 添加动画效果
				animation: float 2s ease-in-out infinite;
			}
		}
		
		// 添加悬浮动画
		@keyframes float {
			0% {
				transform: translateY(0);
			}
			50% {
				transform: translateY(-10rpx);
			}
			100% {
				transform: translateY(0);
			}
		
		
	}
	
	.hot-recommend{
		margin: 20rpx;
	}
	
	.recommend-title{
		display: flex;
		align-items: center;
		/* height: 140rpx; */
		background-color: #f8f8f9;
		border-radius: 0px 10px 10px 0px;
	}
	
	.title-txt{
		display: flex;
		align-items: center;
		justify-content: center;
		width: 240rpx;
		height: 80rpx;
		background-color:#0c34ba;
		/* font-family: "黑体"; */
		/* font-family: "黑体"; */
		font-size:20px;
		color: #fff;
		border-top-right-radius: 40rpx;
		letter-spacing: 1.7px;
	}
	
	.recommend-list{
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		margin-top: 30rpx;
	}
	
	.list-items{
		width: 48%;
		box-sizing: border-box;
		padding: 30rpx;
		background-color: #fff;
		margin-bottom: 30rpx;
		border-radius: 20rpx;
		
	}
	
	.item-picture{
		width:100%;
	}
	
	.picture-show{
		width: 100%;
	}
	
	.items-chinese-name{
		font-size: 38rpx;
		color: #444;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		font-size: 32rpx;
		padding: 3rpx 0;
		letter-spacing: 0.5px;
		font-family: "黑体";
		font-weight: 600;
	}
	
	.items-english-name{
		color: #666;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		font-size: 30rpx;
		padding: 3rpx 0;
		font-family: 'Times New Roman', Times, serif;
		font-weight: 600;
	}
	
	.items-price{
		margin-top: 3px;
	}
	
	.coffee-price{
		color: #0c34ba;
		font-weight: bolder;
		line-height: 4px;
		
	}
	
	.item-picture{
		position: relative;
	}
	
	.item-picture::before{
		content: "hot";
		position: absolute;
		left: 16rpx;
		top: 0;
		color: #fff;
		z-index: 997;
		padding: 2px 8px;
		background-color: #0c34ba;
		font-family: "楷体";
		border-radius: 0 0 10px 10px;
	}
	
</style>
