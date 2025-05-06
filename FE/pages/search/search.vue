<template>
	<view class="search">
		<!-- 搜索结构 -->
		<view class="nav">
			<view class="nav-search-box">
				<view class="nav-left" @click="handleBack">
					<view class="back">
						<u-icon name="arrow-left" color="#0c34ba" size="30"></u-icon>
					</view>
					<view class="back-text">
						返回
					</view>
				</view>
				<view class="nav-right" :style="isFlag?'':'border-radius:50rpx' ">
					<u-icon name="search" color="#0c34ba" size="18"></u-icon>
					<input type="search" confirm-type="search" 
					@confirm="doSearch" v-model="text" class="ipt" placeholder="搜索商品"/>
					<view class="cancel" v-show="isFlag" @click="cancel">
						取消
					</view>
				</view>
			</view>
		</view>
		
		<!-- 背景 -->
		<view class="bg"></view>
		
		<!-- 历史搜索 -->
		<view class="search-history" v-show="!isShowSearchResult">
			<view class="history-top">
				<text>历史搜索</text>
				<image class="delete-picture" src="../../static/delete.png" mode="widthFix" @click="clearHistory" v-if="historyList.length > 0"></image>
			</view>
			<view class="history-items">
				<view class="history-item" v-for="(item, index) in historyList" :key="index" @click="searchGuess(item)">
					{{item}}
				</view>
				<view class="no-history" v-if="historyList.length === 0">
					暂无搜索记录
				</view>
			</view>
		</view>
		
		
		<view class="bg1"></view>
		
		<!-- 猜你想搜 -->
		<view class="search-guess" v-show="!isShowSearchResult">
			<text>活动资讯</text>
			<!-- 活动资讯列表 -->
			<view class="guess-list">
				<view class="list-items" v-for="(item,index) in SearchGuess" :key="index" @click="searchGuess(item.desc)">
					<!-- 图片和文字-->
					<view class="item-picture">
						<image class="picture-show" :src="item.imgUrl" mode="widthFix"></image>
						<view class="desc-show">{{item.desc}}</view>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 商品结构 -->
	<!-- 商品结构 -->
	<view class="product" v-show="isShowSearchResult">
		<image src="../../static/images/网络.png" mode="widthFix" class="img-network" v-show="isShow"></image>
		<view class="product-box" v-for="(item,index) in searchList" :key="index" @click="goToDetail(item)">
			<view class="img-box">
				<image :src="item.smallImg" mode="widthFix" class="img"></image>
			</view>
			<view class="product-name common">
				{{item.name}}
			</view>
			<view class="product-enname common">
				{{item.enname}}
			</view>
			<view class="product-price">
				￥{{item.price}}
			</view>
		</view>
	</view>
		</view>
</template>

<script>
	export default {
		data() {
			return {
				searchList: '',
				isFlag: true,
				text: "",
				isShow: false,
				isShowSearchResult: false,
				SearchGuess: [],
				historyList: []  ,// 新增历史搜索列表
				isFromSearch: true // 添加标记，表示是从搜索页面进入详情
			}
		},
		watch: {
			text() {
				//判断 输入框 是否 为空值
				this.change()
			}
		},
		created() {
			this.getGuess();
			this.loadHistory();  // 加载历史搜索记录
		},
		methods: {
			// 清除搜索状态
					clearSearchState() {
						this.text = '';
						this.searchList = '';
						this.isFlag = false;
						this.isShow = false;
						this.isShowSearchResult = false;
						uni.removeStorageSync('lastSearchState');
					},
			// 添加跳转到详情页的方法
					goToDetail(item) {
						try {
							// 保存当前的搜索状态到本地存储，以便返回时恢复
							uni.setStorageSync('lastSearchState', {
								text: this.text,
								searchList: this.searchList,
								isShowSearchResult: this.isShowSearchResult,
								isFromSearch: true // 添加标记
							});
							
							// 跳转到详情页
							uni.navigateTo({
								url: `/pages/detail/detail?id=${item.pid}`,
								fail: (err) => {
									console.error('跳转失败:', err);
									uni.showToast({
										title: '跳转失败，请重试',
										icon: 'none'
									});
								}
							});
						} catch (e) {
							console.error('保存搜索状态失败:', e);
						}
					},
			// 在页面显示时恢复搜索状态
					onShow() {
    try {
        const lastSearchState = uni.getStorageSync('lastSearchState');
        if (lastSearchState && lastSearchState.isFromDetail) {
            // 如果是从详情页返回，恢复搜索状态
            this.text = lastSearchState.text;
            this.searchList = lastSearchState.searchList;
            this.isShowSearchResult = lastSearchState.isShowSearchResult;
            // 清除状态，防止其他页面进入时还原
            uni.removeStorageSync('lastSearchState');
        }
    } catch (e) {
        console.error('恢复搜索状态失败:', e);
    }
},		
					
			// 加载历史搜索记录
					handleBack() {
    if (this.isShowSearchResult) {
        // 如果正在显示搜索结果，则返回搜索页面
        this.isShowSearchResult = false;
        this.text = '';
        this.isFlag = false;
        // 清除搜索状态
        uni.removeStorageSync('lastSearchState');
    } else {
        // 如果是在搜索页面，则返回上一页并清除搜索状态
        this.clearSearchState();
        uni.navigateBack({
            delta: 1
        });
    }
},
					loadHistory() {
			try {
				const history = uni.getStorageSync('searchHistory');
				this.historyList = history ? JSON.parse(history) : [];
			} catch (e) {
				this.historyList = [];
			}
					},
					
					// 保存搜索记录
					saveHistory(text) {
			if (!text) return;
			try {
				let history = uni.getStorageSync('searchHistory');
				history = history ? JSON.parse(history) : [];
				// 移除重复项
				history = history.filter(item => item !== text);
				// 添加到开头
				history.unshift(text);
				// 最多保存10条
				if (history.length > 10) {
					history = history.slice(0, 10);
				}
				uni.setStorageSync('searchHistory', JSON.stringify(history));
				this.historyList = history;
			} catch (e) {
				console.error('保存历史记录失败:', e);
			}
					},
					
					// 清空历史记录
					clearHistory() {
						uni.showModal({
							title: '提示',
							content: '确定要清空历史记录吗？',
							success: (res) => {
								if (res.confirm) {
									uni.removeStorageSync('searchHistory');
									this.historyList = [];
								}
							}
						});
					},
					
					getSearch(text) {
						this.text = text;
						// 保存搜索记录
						this.saveHistory(text);
						
						uni.showLoading({
							title: "正在加载...",
							mask: true
						});
						uni.request({
							url: "http://newcoffee.wwp666.cn:10006/search",
							data: {
								appkey: "U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
								name: this.text
							},
							success: (res) => {
								if (res.statusCode === 200) {
									this.searchList = res.data.result;
									if (this.searchList == '') {
										uni.showToast({
											title: "未查询到此数据",
											icon: "none",
											mask: true
										});
										this.isShow = true;
									} else {
										this.isShow = false;
									}
									uni.hideLoading();
									this.isShowSearchResult = true;
								}
							}
						});
					},
			getSearch(text) {
				this.text = text
				uni.showLoading({
					title: "正在加载...",
					mask: true
				})
				uni.request({
					url: "http://newcoffee.wwp666.cn:10006/search",
					data: {
						appkey: "U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
						name: this.text
					},
					success: (res) => {
						if (res.statusCode === 200) {
							//获取 数据
							this.searchList = res.data.result
							//判断 数据 是否存在
							if (this.searchList == '') {
								uni.showToast({
									title: "未查询到此数据",
									icon: "none",
									mask: true
								})
								//是否 显示 图片
								this.isShow = true
							} else {
								//是否 显示 图片
								this.isShow = false
							}
							uni.hideLoading()
							this.isShowSearchResult = true
						}
					}
				})
			},
			doSearch() {
				// 通过 回车 获取数据  进行 渲染
				this.getSearch(this.text)
			},
			cancel() {
				this.text = ''
				this.isShowSearchResult = false
				this.isFlag=false
				uni.removeStorageSync('lastSearchState')
			},
			change() {
				//判断  输入框 是否有值
				if (this.text === '') {
					this.isFlag = false
				} else {
					this.isFlag = true
				}
			},
			back() {
				// 返回上一级
				uni.navigateBack({
					delta: 1
				})
			},
			getGuess(){
				uni.request({
					url:" https://mock.mengxuegu.com/mock/63ff40f17c016026ff2b92a0/searchguess",
					method:"GET",
					data:{
						appkey:"U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
						key:"isHot",
						value:1
					},
					success:(res)=> {
						// console.log("res=>",res);
						this.SearchGuess=res.data.data;
						// console.log("data下的SearchGuess重新赋值=>",this.SearchGuess);
					}
				})
			},
			searchGuess(desc) {
				this.text = desc
			 this.getSearch(desc)
			}
		},
		onLoad(option) {
		    // 如果不是从详情页返回，则清除搜索状态
		    const lastSearchState = uni.getStorageSync('lastSearchState');
		    if (!lastSearchState || !lastSearchState.isFromDetail) {
		        this.clearSearchState();
		    }
		    
		    if(option.text) {
		        this.getSearch(option.text);
		        this.isShowSearchResult = true;
		    }
		    this.change();
		    this.loadHistory();  // 确保历史记录被加载
		}
	}
</script>

<style lang="less" scoped>
	.search {
		height: 100vh;
		background-color: #f7f7f7;

		// 顶部 搜索 样式
		.nav {
			height: 100rpx;
			padding: 0 30rpx;
			background-color: #fff;
			display: flex;
			align-items: center;
			position: relative;
			z-index: 1;

			.nav-search-box {
				width: 100%;
				height: 70rpx;
				display: flex;

				.nav-left {
					margin-right: 30rpx;
					flex: 2;
					display: flex;
					justify-content: center;


					.back {
						line-height: 70rpx;
						margin-right: 10rpx;
					}

					.back-text {
						color: #0c34ba;
						font-size: 28rpx;
						line-height: 70rpx;
					}
				}

				.nav-right {
					border-radius: 50rpx 0 0 50rpx;
					padding-left: 20rpx;
					background-color: #f7f8fa;
					flex: 8;
					display: flex;
					justify-content:space-between;
					align-items: center;
					.ipt{
						flex: 1;
					}
					.cancel {
						width: 100rpx;
						padding-right: 20rpx;
						background-color: #fff;
						text-align: center;
						line-height: 70rpx;
					}

				}


			}
		}

	.search-history {
		padding: 15px 15px;
		font-weight: bold;
		background: #efeff0;
		
		.history-top {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 15px;
		}
		
		.delete-picture {
			width: 23px;
			position: absolute;
			right: 24px;
		}
		
		.history-items {
			display: flex;
			flex-wrap: wrap;
			gap: 10px;
			
			.history-item {
				padding: 8px 15px;
				background-color: #fff;
				border-radius: 20px;
				font-size: 14px;
				color: #666;
			}
		}
	}

		//背景颜色
		.bg {
		height: 100rpx; // 减小蓝色背景高度
		background-color: #0c34ba;
		margin-bottom: -60rpx; // 添加负边距，让下面的内容上移
		}
		.bg1 {
		height: 95rpx; // 减小蓝色背景高度
		background-color: #0c34ba;
		margin-bottom: -60rpx; // 添加负边距，让下面的内容上移
		}

		// 猜你想搜样式
		.search-guess {
			padding: 15px 15px;
			font-weight: bold;
			background-color: #efeff0;
		}
		
		.guess-list {
			display: flex;
			flex-wrap: wrap;
			justify-content: space-between;
			margin-top: 30rpx;
		}
		
		.list-items {
			/* border: 2px solid red; */
			display: flex;
			justify-content: center;
			box-sizing: border-box;
			background-color: #fff;
			margin-bottom: 10px;
			border-radius: 20px;
		}
		
		.picture-show {
			width: 340px;
			border-radius: 20px;
			
		}
		
		.desc-show {
			overflow: hidden;
			margin-top: 5px;
			margin-bottom: 5px;
			margin-left: 10px;
			font-family: "黑体";
			letter-spacing: 1px;
			color: #1f2981;
			
		}
		
		// 历史搜索样式
		.seaech-history {
		position: relative;
		margin: 0 30rpx;
		padding: 30rpx;
		background: #fff;
		border-radius: 20rpx;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
		}
		
		.history-top {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 20rpx;
			
			text {
							font-size: 32rpx;
							font-weight: bold;
							color: #333;
						}
		}
		
		/*.delete-picture {
			width: 40rpx;
			height: 40rpx;
		}*/
		
		.histori-items {
			display: flex;
			flex-wrap: wrap;
			gap: 20rpx;
			
			.history-item {
				padding: 10rpx 30rpx;
				background-color: #f7f7f7;
				border-radius: 30rpx;
				font-size: 28rpx;
				color: #666;
				
				&:active {
					background-color: #e0e0e0;
				}
			}
			
			.no-history {
				width: 100%;
				text-align: center;
				color: #999;
				font-size: 28rpx;
				padding: 40rpx 0;
			}
		}

		// 商品结构 样式
		.product {
			position: relative;
			top: -50rpx;
			border-radius: 30rpx 30rpx 0 0;
			padding: 20rpx;
			padding-left: 5rpx;
			margin: 0 30rpx;
			background-color: #fff;
			display: flex;
			flex-wrap: wrap;

			.img-network {
				width: 100%;
				display: block;
			}

			.product-box {
			width: 200rpx;
			margin-left: 20rpx;
			margin-bottom: 20rpx;
			// 添加点击效果
			&:active {
				opacity: 0.8;
				transform: scale(0.98);
			}
			// 添加过渡效果
			transition: all 0.2s ease;
			
			// 添加点击反馈
			&:active {
				background-color: rgba(0, 0, 0, 0.05);
			}

				.img-box {
					height: 200rpx;

					.img {
						width: 100%;
						display: block;
					}
				}

				.common {
					text-align: start;
					display: -webkit-box;
					white-space: pre-wrap;
					overflow: hidden;
					text-overflow: ellipsis;
					-webkit-box-orient: vertical;
					-webkit-line-clamp: 1;
				}

				.product-name {

					font-size: 36rpx;
					color: #646566;
					margin: 10rpx 0;
				}

				.product-enname {
					font-size: 28rpx;
					color: #999;
					margin: 10rpx 0;

				}

				.product-price {
					color: #0c34ba;
					font-size: 32rpx;
					font-weight: bold;
				}
			}
		}
	}
</style>
