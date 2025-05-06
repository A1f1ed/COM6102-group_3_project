<template>
	<view class="menu-home" >
		<!-- 搜索框 -->
		<view class="nav-search" >
			<u-search placeholder="输入商品名称" v-model="keyword" :showAction="false" search-icon-color="#0c34ba"
				searchIconSize=26 maxlength=15 :disabled="true" @click="gotoSearch()">

			</u-search>
		</view>
	
		<view class="menu">
			<view class="menu-type">
				<view class="type-list" v-for="(item,index) in typeList" :key="item.id">
					<view class="type-picture" @click="getProductList(index,item.key,item.type)">
						<image class="picture-show" :src="item.isActive ? item.activeImg : item.img" mode="widthFix">
						</image>
					</view>
					<view class="type-name" :class="item.isActive ? 'active' : ''" >{{item.typeDesc}}
						
					</view>
				</view>
			</view>
			
			
			<view class="menu-products">
			<view class="product-list" v-for="(item,index) in typeProductList" :key="index" @click="gotoDetails(item.pid,item.type)">
					<view class="list-left">
						<image class="left-picture" :src="item.smallImg" mode="widthFix"></image>
						<view class="left-name">
							<view class="chinese-name">{{item.name}}	
							</view>
							<view class="english-name">{{item.enname}}	
							</view>
						</view>
						
							
						</view>
						<view class="list-right">&yen; {{item.price}}
					</view>
				</view>
				
			</view>
		</view>
	</view>
</template>

<script>

	
	export default {
		data() {
			return {
				keyword: "",

				typeList: [{
						img: "../../static/menuIcon/icons_01.png",
						activeImg: "../../static/menuIcon/icons_02.png",
						isActive: false,
						key: "isHot"
					},
					{
						img: "../../static/menuIcon/icons_03.png",
						activeImg: "../../static/menuIcon/icons_04.png",
						isActive: false,
						key: "type"
					},
					{
						img: "../../static/menuIcon/icons_05.png",
						activeImg: "../../static/menuIcon/icons_06.png",
						isActive: false,
						key: "type"
					},
					{
						img: "../../static/menuIcon/icons_07.png",
						activeImg: "../../static/menuIcon/icons_08.png",
						isActive: false,
						key: "type"
					},
					{
						img: "../../static/menuIcon/icons_09.png",
						activeImg: "../../static/menuIcon/icons_10.png",
						isActive: false,
						key: "type"
					}
				],
			
				typeProductList:[]
			}
		},
		created() {
			this.getType();
			this.getProductList(0,'isHot',1);
		},

		methods: {
			gotoSearch(){
				uni.navigateTo({
					url:"../../pages/search/search"
				})
			},
			
			getType() {
				this.$uni({
					url: "/type"
				}).then(res => {
					// console.log("第一次获取商品类型==>", res);
					let hot ={
						id:0,
						typeDesc:"推荐",
						type:1
					}
					res.unshift(hot);
					// console.log("第二次获取商品类型==>",res);
					let arr = [];
					let obj = {};
					res.forEach((item,index)=>{
						obj={
							...item,
							...this.typeList[index]
						}
						arr.push(obj);
					})
					// console.log("第三次获取商品类型==>",res);
					this.typeList=arr;
					// console.log("第四次获取商品类型==>",this.typeList);
				})
			},
		
			getProductList(index,key,value){
				if(this.typeList[index].isActive){
					return;
				}
				
				this.$uni({
					url:"/typeProducts",
					data:{
						key,
						value
					}
				}).then(res => {
					// console.log("菜单页面是否获取到指定商品类型的数据=》",res);
					this.typeProductList = res;
					// console.log("当前点击的是类型为：" + value + " 的列表数据为：",this.typeProductList);
					
					// 排他思想
					this.typeList.forEach(item=>{
						item.isActive=false;
					})
					this.typeList[index].isActive=true;
				})
			},
			gotoDetails(pid,type){
				// console.log("点击具体的一个商品 pid=>",pid);
				// console.log("点击具体一个商品 type=>",type);
				uni.navigateTo({
					url:"/pages/detail/detail?id="+ pid
				})
			}
		}
	}
</script>

<style>
	.menu-home{
		
	}
	
	/deep/.u-search__content {
		display: flex;
		align-items: center;
		justify-content: center;
		margin: 16px;
	}
	
	.menu-type{
		display: flex;
		justify-content: space-evenly;
		text-align: center;
		padding: 20rpx 0;
		background-color: #fbfafa;
		position: sticky;
		top: 0;
		z-index: 9999;
	}
	
	/deep/.uni-page-wrapper{
		background-color: #efeff0;
	}
	
	.u-search{
		background-color: #fff;
	}
	
	.picture-show{
		width: 70rpx;
	}
	
	.type-name{
		font-weight: bold;
		font-size: 28rpx;
	}
	
	.active{
		color:#0a22ba;
	}
	
	/* 商品类型对应的列表数据 */
	.menu-products{
		padding-bottom:50rpx;
		/* 正式颜色 */
		border-top:1rpx solid #efeff0;
		background-color:#efeff0;
		/* 测试颜色 */
/* 		border-top:1rpx solid skyblue;
		background-color:skyblue; */
		
	}
	
	.product-list{
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 26rpx;
		margin: 32rpx;
		background-color: #fff;
		border-radius: 10rpx;
	}
	
	/*  */
	.product-list:last-child{
		margin-bottom:0;
	}
	
	.list-left{
		display: flex;
		align-items: center;
		flex-basis: 80%;
		position: relative;
	}
	
	.left-picture{
		width:160rpx;
		min-width: 160rpx;
		margin-right: 20rpx;
		border-radius: 6rpx;
	}
	
	.left-name{
		position: absolute;
		left: 180rpx;
		width: 60%;
		color: #6f6f70;
	}
	
	.chinese-name,.english-name{
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		letter-spacing: 0.5px;
		font-family: "黑体";
		font-weight: 600;
		color: #666
	}
	
	.english-name{
		padding-top: 10rpx;
		font-size: 26rpx;
		font-family: 'Times New Roman', Times, serif;
		font-weight: 600;
		
	}
	
	.list-right{
		flex-basis: 20%;
		min-width: 136rpx;
		font-weight: bold;
		color: #0a33ba;
		font-size: 28rpx;
	}
</style>
