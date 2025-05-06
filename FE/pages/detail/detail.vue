<template>
	<view class="detail">
		
		<!-- 导航栏 -->
			<view class="navbar-top">
				<u-navbar
				:safeAreaInsetTop="false"
				title="商品详情"
				color="#0c34ba"
				:fixed="false"
				left-text="返回"
				@leftClick="backIndex">
				</u-navbar>
			</view>
	
		<!-- 商品图 -->
		<view class="big-img">
			<image :src="detail.large_img" mode="widthFix" class="b-img"></image>
		</view>
		
		<!-- 中间详情卡片 -->
		<view class="content">
			<!-- 商品信息 -->
			<view class="info">
				<view class="info-name">
					<view class="info-chname">{{detail.name}}</view>
					<view class="info-enname">{{detail.enname}}</view>
				</view>
				<view class="info-price">￥{{detail.price}}</view>
			</view>
			
			<!-- 类型规格 -->
			<view class="type">
				<view class="type-list" v-for="(item,index) in detail.infoArr" :key="index">
					<view class="type-title">{{item.name}}</view>
					<view class="type-detail">
						<view class="type-detail-list" v-for="(it,id) in item.info" :key="id">
							<view class="type-list-name" :class="it.isActive?'active':''" @click="toggle(index,id)">
								{{it.name}}
							</view>
						
						</view>
					</view>
				</view>
			</view>
			
			<!-- 步进器 -->
			<view class="count">
				<view class="count-name">选择数量</view>
				<view class="step">
					<view class="step-left" @click="countNum(-1)">-</view>
					<view class="step-center">{{num}}</view>
					<view class="step-right" @click="countNum(1)">+</view>
				</view>
			</view>
			
			<!-- 商品描述 -->
			<view class="desc">
				<view class="desc-title">商品描述</view>
				<view class="desc-list" v-for="(item,index) in detail.descArr" :key="index">{{index+1}}、{{item}}</view>
			</view>
			
			<!-- 底部栏 -->
				<u-tabbar
					:value="value1"
					:fixed="true"
					:placeholder="true"
					:safeAreaInsetBottom="true"
					@change="change1"
					activeColor="#0c34ba"
					>
					<u-tabbar-item text="购物袋" :badge="badge" @click="goCar()">
						<image
							class="u-page__item__slot-icon"
							slot="active-icon"
							src="../../static/shop_active.png"
							mode="widthFix"
						></image>
						<image
						class="u-page__item__slot-icon"
						slot="inactive-icon"
						src="../../static/shop.png"
						mode="widthFix"
						></image>
					</u-tabbar-item>
					<u-tabbar-item text="收藏"    @click="click1">
						<image
							class="u-page__item__slot-icon"
							slot="active-icon"
							src="../../static/like_active.png"
							mode="widthFix"
						></image>
						<image
						class="u-page__item__slot-icon"
						slot="inactive-icon"
						src="../../static/like.png"
						mode="widthFix"
						></image>
					</u-tabbar-item>
					<view class="tab-right">
						<text class="tab-car" @click="addCar()">加入购物袋</text>
						<text class="tab-buy">立即购买</text>
					</view>
					</u-tabbar>
			
		</view>
	</view>
</template>

<script>
import search from '../../uni_modules/uview-ui/libs/config/props/search';

	export default {
		data() {
			return {
				fromSearch: false,
				value1: 0,
				//商品pid
				pid: "",
				//商品详情
				detail: {},
				// 购物车徽标
				badge:"",
				//类型
				typeList: ['cream_desc', 'milk_desc', 'sugar_desc', 'tem_desc'],

				// options: [{
				// 	icon: 'cart',
				// 	text: '购物袋',
				// 	info: 0,
				// 	infoBackgroundColor: '#0c34ba',
				// 	infoColor: "#f5f5f5"
				// }, {
				// 	icon: 'heart',
				// 	text: '未收藏'
				// }],
				// ButtonGroup: [{
				// 		text: '加入购物车',
				// 		backgroundColor: '#6a91ec',
				// 		color: '#fff'
				// 	},
				// 	{
				// 		text: '立即购买',
				// 		backgroundColor: '#0c34ba',
				// 		color: '#fff'
				// 	}
				// ],
				//数量
				num: 1
			};
		},
		onLoad:function(options) {
			// console.log("获取options.id",options.id);
			//更新初始数据里面的pid
			this.fromSearch = options.fromSearch === 'true';
			this.pid = options.id
			//调用商品详情方法
			this.getDetail()
		},
		methods: {
		backIndex() {
			if (this.fromSearch) {
				// 如果是从搜索页面进入，则返回搜索页面
				uni.navigateTo({
					url:"/pages/search/search"
				})
			} else {
				// 如果不是从搜索页面进入，则正常返回
				uni.navigateBack({
					delta: 1
				});
			}
		},
		
		// 监听物理返回按钮（针对Android设备）
		onBackPress() {
			if (this.fromSearch) {
				// 如果是从搜索页面进入，则返回搜索页面
				uni.navigateBack({
					delta: 1
				});
				return true; // 返回true，表示自己处理返回逻辑
			}
			return false; // 返回false，表示使用默认返回逻辑
		},
			
			//设置获取商品详情数据
			getDetail() {
				//开始发送网络请求
				this.$uni({
					//开发者服务器接口地址
					url: "/productDetail",
					data: {
						pid: this.pid
					}
				}).then(res => {
					// console.log("商品详情", res);
					this.detail = res[0]
					//开始处理描述数据
					let descArr = res[0].desc.split("\n")
					// console.log("处理描述数据", descArr);
					//开始处理规格数据
					let infoArr = [];
					//对类型数组进行遍历
					this.typeList.forEach(item => {
						//获取具体规格
						let info = res[0][item.split("_")[0]].split("/");
						// console.log("info", info);
						//判断规格详情是否是空的
						if (info[0] == "") {
							return
						}
						// console.log("item", item, res[0][item]);
						//存放具体规格对象数组
						let typeList = []
						info.forEach((item, index) => {
							// console.log("item-info", item);
							let type = {
								name: item,
								isActive: index == 0 ? true : false
							}
							typeList.push(type)
						})
						let obj = {
							name: res[0][item],
							info: typeList
						}
						//把新对象添加进空数组
						infoArr.push(obj)
					})
					// console.log("处理的规格数据", infoArr);
					//赋值添加
					this.detail.infoArr = infoArr;
					this.detail.descArr = descArr;
					console.log("最终的商品详情", this.detail);
				})
			},
			//步进器
			countNum(num) {
				if (this.num == 1 && num == -1) {
					return
				}
				this.num = this.num + num;
				// console.log("此时的num => ",this.num);
			},
			// 
			/*addCar(){
				// console.log("此时的num => ",this.num);
				this.badge = this.num;
				uni.showToast({
									title: "成功加入购物袋"
								})
			},*/
			// 在 detail.vue 中修改 addCar 方法
			goCar(){
				setTimeout(() => {
				    uni.reLaunch({
				        url: "/pages/cart/cart"
				    });
				}, 1500);
				uni.showToast({
				    title: "正在全速前进了",
				    icon: 'loading',
				    duration: 2000
				});
			},
			addCar() {
			    try {
			        if (this.num <= 0) {
			            this.handleError('商品数量不能为0');
			            return;
			        }
			        
			        // 获取当前选中的规格
			        const selectedSpecs = this.detail.infoArr.map(item => {
			            const selected = item.info.find(it => it.isActive);
			            return {
			                name: item.name,
			                value: selected ? selected.name : ''
			            };
			        });
			
			        // 构建购物车商品信息
			        const cartItem = {
			            pid: this.pid,
			            name: this.detail.name,
			            price: this.detail.price,
			            large_img: this.detail.large_img,
			            num: this.num,
			            specs: selectedSpecs,
						selected:false
			        };
			
			        // 获取现有的购物车数据
			        let cartItems = [];
			        try {
			            const itemsStr = uni.getStorageSync('cartItems');
			            if (itemsStr) {
			                cartItems = JSON.parse(itemsStr);
			            }
			        } catch (error) {
			            console.error('读取购物车数据错误:', error);
			        }
			
			        // 检查是否已存在相同商品
			        const existingIndex = cartItems.findIndex(item => 
			            item.pid === cartItem.pid && 
			            JSON.stringify(item.specs) === JSON.stringify(cartItem.specs)
			        );
			
			        if (existingIndex !== -1) {
			            cartItems[existingIndex].num += cartItem.num;
			        } else {
			            cartItems.push(cartItem);
			        }
			
			        // 保存到本地存储
			        try {
			            uni.setStorageSync('cartItems', JSON.stringify(cartItems));
			            this.badge = cartItems.reduce((total, item) => total + item.num, 0);
			            
			            uni.showToast({
			                title: "成功加入购物袋",
			                icon: 'success',
			                duration: 2000
			            });
			
			            /*setTimeout(() => {
			                uni.reLaunch({
			                    url: "/pages/cart/cart"
			                });
			            }, 1500);*/
			        } catch (error) {
			            console.error('保存购物车数据错误:', error);
			            this.handleError('加入购物袋失败');
			        }
			
			    } catch (error) {
			        console.error('加入购物车错误:', error);
			        this.handleError('加入购物袋失败');
			    }
			},
			//切换规格
			// 切换规格
			toggle(index, id) {
			    try {
			        // 检查数据有效性
			        if (!this.detail.infoArr || !this.detail.infoArr[index]) {
			            this.handleError('规格数据无效');
			            return;
			        }
			
			        const info = this.detail.infoArr[index].info;
			        if (!info || !info[id]) {
			            this.handleError('规格选项无效');
			            return;
			        }
			
			        // 更新选中状态
			        info.forEach((item, i) => {
			            item.isActive = i === id;
			        });
			
			        // 强制更新视图
			        this.$forceUpdate();
			        
			        // 可以在这里添加规格变化后的其他逻辑
			        console.log('当前选中的规格：', {
			            type: this.detail.infoArr[index].name,
			            value: info[id].name
			        });
			    } catch (error) {
			        this.handleError('切换规格失败');
			    }
			},

			//输入框事件
			input(keyword) {
				// console.log("现在触发", keyword);
			},
			
			// 底部购物车和收藏
			change1(e) {
				this.value1 = e
				// console.log('change1', e);
						},
			click1(e) {
				// console.log('click1', e);
						}
		}
	}
</script>

<style lang="scss">
	.detail{
		background-color: #efeff0;
	}
	
	.uni-page-wrapper{
		background-color: #efeff0;
	}
	
	/deep/.u-navbar__content[data-v-95dec1ae]{
		padding: 8px;
		}
	
	.big-img{
		display: flex;
		justify-content: center;
	}
	.b-img {
		// height: 280px;
		width: 375px;
	}

	.bottom {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		z-index: 99;
	}

	.content {
		background-color: #fff;
		margin: 0 10px;
		border-radius: 10px;
		position: relative;
		top: -25px;
		padding: 15px;
	}

	.info {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 5px;
	}

	.info-chname {
		font-size: 16px;
		color: #6d6e6f;
		font-weight: bold;
		font-size: 36rpx;
		font-family: "黑体";
		letter-spacing: 1px;
	}

	.info-enname {
		font-size: 13px;
		color: #6d6e6f;
		font-size: 32rpx;
		font-family: 'Times New Roman', Times, serif;

	}

	.info-price {
		font-size: 20px;
		color: #0c34ba;
		font-weight: bold;
	}

	.type-list {
		display: flex;
		margin-bottom: 10px;
	}

	.type-detail {
		display: flex;
	}

	.type-title {
		width: 60px;
		font-size: 16px;
		font-weight: bold;
		padding-left: 5px;
		padding-top: 5px;
		display: flex;
		// justify-content: center;
	}

	.type-list-name {
		padding: 8px 5px;
		width: 60px;
		background-color: #e8e8e8;
		margin-right: 10px;
		text-align: center;
		border-radius: 15px;
		font-size: 14px;
	}

	.type-list-name.active {
		background-color: #0c34ba;
		color: #fff;
	}


	::v-deep .uni-navbar__header[data-v-6bda1a90] {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		z-index: 99;
	}

	.count {
		display: flex;
		border-top: 1px solid #ddd;
		border-bottom: 1px solid #ddd;
		align-items: center;
		justify-content: space-between;
		margin-top: 25px;
		padding: 15px 0;
		
	}
	
	.count-name{
		font-weight: bold;
	}
	
	.step {
		display: flex;
	}

	.step-left,
	.step-right {
		width: 20px;
		height: 20px;
		background-color: #0c34ba;
		border-radius: 50%;
		color: #fff;
		text-align: center;
		line-height: 20px;
	}

	.step-center {
		margin: 0 10px;
		color: #333;
	}

	.step-left {
		background-color: #fff;
		color: #666;
		border: 1px solid #666;
		box-sizing: border-box;
	}

	.desc-title {
		margin: 15px 0;
		font-weight: bold;
	}

	.desc-list {
		font-size: 13px;
		color: #a0a0a0;
		margin-bottom: 5px;
	}
	
	.u-page__item__slot-icon{
		width: 25px;
	}

	.tab-right{
		padding: 15px;
	}
	
	.tab-car{
		background-color: #6a91ec;
		padding: 8px;
		border-radius: 20px 0px 0px 20px;
		// font-weight: bold;
		color: #fff;
		padding:10px ;
		font-family: "黑体";
		 
	}
	
	.tab-buy{
		background-color:#0c34ba;
		// padding: 8px;
		border-radius: 0px 20px 20px 0px;
		// font-weight: bold;
		color: #fff;
		// margin-right: 4px;
		padding:10px ;
		font-family: "黑体";
		
	}
	
</style>
